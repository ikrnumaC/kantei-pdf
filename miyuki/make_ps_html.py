#!/usr/bin/env python3
"""深雪のPS文(txt)からPSページ(HTML)を作り、URLを miyukihonshiki.txt に登録する。

使い方（Claudeが実行する。手では動かさない）:
    python3 miyuki/make_ps_html.py 有料鑑定/深雪/1662_でぃあ様_本式守護鑑定/1662_でぃあ_PS.txt

やること:
    1. miyuki/連番_名前様PS/index.html を作る（CSS・フッターは1662のひな形から取る）
    2. 石の画像(miyuki/素材)が実在するか、プレースホルダ等が残っていないか検査する
    3. miyuki/miyukihonshiki.txt に PS のURL行がなければ追記する
"""
import html
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "1662_でぃあ様PS" / "index.html"
URL_LIST = ROOT / "miyukihonshiki.txt"
BASE_URL = "https://kantei-pdf.pages.dev/miyuki/"

STONE_IMG = {
    "カーネリアン": "カーネリアン", "シトリン": "シトリン", "黄水晶": "シトリン",
    "ジェイド": "ヒスイ", "翡翠": "ヒスイ", "ヒスイ": "ヒスイ",
    "アクアマリン": "アクアマリン",
    "アベンチュリン": "アベンチュリン", "グリーンアベンチュリン": "アベンチュリン",
    "スモーキークォーツ": "スモーキークォーツ", "タイガーアイ": "タイガーアイ",
    "ルチルクォーツ": "ルチルクォーツ", "シルバールチルクォーツ": "ルチルクォーツ",
    "ローズクォーツ": "ローズクォーツ", "ムーンストーン": "ムーンストーン",
    "ラピスラズリ": "ラピスラズリ", "ラリマー": "ラリマー", "ラブラドライト": "ラブラドライト",
    "アメジスト": "アメジスト", "ガーネット": "ガーネット", "クリアクォーツ": "クリアクォーツ",
    "ペリドット": "ペリドット",
}
SECTION_EMOJI = "💎🪨✨⏰📦🎁"


def esc(s):
    return html.escape(s, quote=False)


def para(block):
    return "<p>" + "<br>".join(esc(l) for l in block) + "</p>"


def paras(blocks, indent="    "):
    out = []
    for i, b in enumerate(blocks):
        if i:
            out.append(indent + "<br>")
        out.append(indent + para(b))
    return out


def split_blocks(lines):
    """空行区切りのブロック(行のリスト)に分ける。"""
    blocks, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l.strip())
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return blocks


def stone_key(name):
    base = re.sub(r"（.*?）|\(.*?\)", "", name).strip()
    return base if base in STONE_IMG else None


def build_body(text, errors):
    # ━━ 区切りでセクションに分ける
    sections = [s.splitlines() for s in re.split(r"^━+\s*$", text, flags=re.M)]
    sections = [s for s in sections if any(l.strip() for l in s)]
    out = ['  <div class="body">']

    # 先頭: 名前〜導入
    intro = split_blocks(sections[0])
    out += paras(intro)
    name_m = re.match(r"(.+?)様", intro[0][0])
    name = name_m.group(1) if name_m else ""
    out.append('    <hr class="divider">')

    last = len(sections) - 1
    for idx, sec in enumerate(sections[1:], start=1):
        blocks = split_blocks(sec)
        head = blocks[0][0]
        if idx == last and head[0] not in SECTION_EMOJI:
            out += build_closing_section(blocks, errors)
            break
        if head[0] not in SECTION_EMOJI:
            errors.append(f"見出しの絵文字がないセクション: {head}")
            continue
        title = head
        rest = [blocks[0][1:]] + blocks[1:] if len(blocks[0]) > 1 else blocks[1:]
        out.append(f'    <div class="section-title">{esc(title)}</div>')
        if title[0] == "🪨":
            out += build_stones(sec, errors)
        elif title[0] == "✨":
            out += build_bracelet(title, rest, errors)
        elif title[0] == "📦":
            out.append('    <ul class="info-list">')
            for b in rest:
                for l in b:
                    out.append(f"      <li>{esc(l.lstrip('・'))}</li>")
            out.append("    </ul>")
        elif title[0] == "🎁":
            out += build_tokuten(rest)
        else:
            out += paras(rest)
        out.append('    <hr class="divider">')
    return "\n".join(out), name


def build_stones(sec, errors):
    out = []
    first = next(i for i, l in enumerate(sec) if l.strip())
    lines = sec[first + 1:]  # 見出し行を除く
    entries, cur = [], []
    for l in lines:
        if l.strip() == "---":
            entries.append(cur)
            cur = []
        else:
            cur.append(l)
    entries.append(cur)
    for i, e in enumerate(entries):
        blocks = split_blocks(e)
        if not blocks:
            continue
        stone = blocks[0][0]
        key = stone_key(stone) if len(blocks[0]) == 1 else None
        if not key:
            errors.append(f"石名として認識できない/画像対応がない: {blocks[0][0]}")
            continue
        if i:
            out.append('    <div class="stone-divider"></div>')
        out.append(f'    <div class="stone-title">{esc(re.sub(r"（.*?）", "", stone))}</div>')
        img = f"{STONE_IMG[key]}.png"
        if not (ROOT / "素材" / img).exists():
            errors.append(f"画像がない: miyuki/素材/{img}")
        out.append(f'    <img src="../素材/{img}" class="stone-img" alt="{esc(key)}">')
        out += paras(blocks[1:])
    return out


def build_bracelet(title, rest, errors):
    out = []
    price = None
    body = []
    for b in rest:
        if b[0].startswith("価格"):
            price = re.search(r"([\d,]+)円", b[0])
        else:
            body.append(b)
    if not price:
        errors.append("価格行がない")
    else:
        label = re.sub(r"^[^\w]*", "", title).strip()
        out += [
            '    <div class="price-box">',
            f'      <div class="price-label">{esc(label)}</div>',
            f'      <div class="price-num">¥{price.group(1)}</div>',
            '      <div class="price-tax">（税込）</div>',
            "    </div>",
        ]
    return out + paras(body)


def build_tokuten(rest):
    out = []
    items = []
    for b in rest:
        for l in b:
            m = re.match(r"(\d+)\.\s*(.+)", l)
            if m:
                items.append((m.group(1), m.group(2)))
            else:
                out += paras([[l]])
                out.append("    <br>")
    out.append('    <div class="tokuten">')
    out.append("      <ul>")
    for n, t in items:
        out.append(f'        <li data-num="{n}">{esc(t)}</li>')
    out += ["      </ul>", "    </div>"]
    return out


def build_closing_section(blocks, errors):
    """購入リンク〜結びの言葉〜署名。"""
    out = []
    url = None
    pre, post = [], []
    for b in blocks:
        if len(b) == 1 and b[0].startswith("http"):
            url = b[0]
        elif url is None:
            pre.append(b)
        else:
            post.append(b)
    if not url:
        errors.append("購入URLがない")
        return out
    out.append("    <p>ご希望の方は、下のボタンよりお進みください。</p>")
    out.append("    <br>")
    out.append(f'    <a href="{esc(url)}" class="cta-button" target="_blank" rel="noopener">ブレスレットを希望する</a>')
    out.append('    <p class="cta-note">※ 別ウィンドウで購入ページが開きます</p>')
    out.append("")

    sign = None
    if post and post[-1] == ["深雪"]:
        sign = post.pop()
    elif post and post[-1][-1] == "深雪":
        post[-1] = post[-1][:-1]
        sign = ["深雪"]
    if sign is None:
        errors.append("署名『深雪』がない")

    # 「ご不明な点があれば」ブロックまでは通常の段落、それ以降は closing
    cut = next((i for i, b in enumerate(post) if b[0].startswith("ご不明な点")), None)
    if cut is None:
        normal, closing = post[:-1], post[-1:]
    else:
        normal, closing = post[: cut + 1], post[cut + 1 :]
    out += paras(normal)
    out.append("")
    out.append('    <div class="closing">')
    out.append("    <p>" + "<br><br>".join("<br>".join(esc(l) for l in b) for b in closing) + "</p>")
    out.append('      <div class="closing-sign">深雪</div>')
    out.append("    </div>")
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit("使い方: make_ps_html.py <連番_名前_PS.txt>")
    src = Path(sys.argv[1]).resolve()
    m = re.match(r"(\d+)_(.+)_PS\.txt$", src.name)
    if not m:
        sys.exit(f"ファイル名が『連番_名前_PS.txt』の形ではありません: {src.name}")
    folder = f"{m.group(1)}_{m.group(2)}様PS"
    text = src.read_text(encoding="utf-8")

    errors = []
    for pat, msg in [(r"【.*?】", "プレースホルダ【】が残っている"), (r"──", "『──』が使われている"),
                     (r"性（さが）|さが）", "『性（さが）』表現がある")]:
        if re.search(pat, text):
            errors.append(msg)

    body, name = build_body(text, errors)
    tpl = TEMPLATE.read_text(encoding="utf-8")
    head = tpl[: tpl.index('  <div class="body">')]
    foot = tpl[tpl.index('  <div class="footer">'):]
    result = head.rstrip("\n") + "\n" + body + "\n  </div>\n" + foot

    if name and name != m.group(2):
        print(f"注意: 本文の名前『{name}』とファイル名の名前『{m.group(2)}』が違います")
    if errors:
        print("エラー（HTMLは作りません）:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    out_dir = ROOT / folder
    out_dir.mkdir(exist_ok=True)
    (out_dir / "index.html").write_text(result, encoding="utf-8")
    print(f"作成: miyuki/{folder}/index.html")

    url = BASE_URL + urllib.parse.quote(folder) + "/"
    line = "PS" + url
    lines = URL_LIST.read_text(encoding="utf-8").splitlines()
    if line in lines:
        print("URL登録済み:", url)
    else:
        with URL_LIST.open("a", encoding="utf-8") as f:
            if lines and not URL_LIST.read_text(encoding="utf-8").endswith("\n"):
                f.write("\n")
            f.write(line + "\n")
        print("URL追記:", url)
    print("返信文に入れるURL:", url)


if __name__ == "__main__":
    main()
