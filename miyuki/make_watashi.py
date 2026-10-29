#!/usr/bin/env python3
# ============================================================
# 深雪 本鑑定 お渡しメッセージ作成スクリプト
#
# 使い方:
#   python3 make_watashi.py 1616 1524     … 指定した連番のお渡し文を作る
#
# 動作:
#   - 有料鑑定/深雪/{連番}_*/ の本鑑定文txt(_v2 等は新しい方)を claude に読ませる
#   - 安心させる一言 + マイナス面を軽く匂わせる一言 + 「中身を視ないと分からない」
#     の長めのメッセージを作り、本鑑定のURLを付ける
#   - URLは miyukihonshiki.txt にあればそれを、無ければ
#     https://kantei-pdf.pages.dev/miyuki/{連番}_{名前}様_本式守護鑑定/ を組み立てる
#     (HTMLはまだ無くてもOK。公開後にこのURLで開く)
#   - miyuki_watashi.txt を毎回上書き(今回指定した分だけが入る)
#   → このtxtの中身をコピーしてそのままLINEに貼る
# ============================================================
import glob, os, re, subprocess, sys, urllib.parse

REPO = "/Users/miura/Documents/GitHub/kantei"
URLS = f"{REPO}/miyuki/miyukihonshiki.txt"
SRC = f"{REPO}/有料鑑定/深雪"
OUT = f"{REPO}/miyuki/miyuki_watashi.txt"
BASE = "https://kantei-pdf.pages.dev/miyuki/"

RULES = """下の深雪の本鑑定文を読んで、お客様に本鑑定書をお渡しするときのLINEメッセージの「中ほどの文章」を作ってください。
冒頭の「おまたせいたしました。」と、末尾の「詳しくは鑑定書に書きました」の一文、URL、公式LINE・DMの案内は私が前後に固定で付けるので、書かないでください。

【内容の組み立て】
1. 結論: 相談内容への答えを、鑑定文全体を読んだうえで「要約」して伝える。鑑定文の文を抜き出して並べるのではなく、あなたの言葉でひとつの流れる文章にまとめる。結論は断定してよい(可否・大まかな時期・相性など)が、盛り込むのは一番大事なことだけに絞る
2. 注意: 気づいていない注意点があれば、「ひとつだけ、お伝えしておきたいことも視えました」と一文で軽く触れる。怖がらせない
3. 締め: 「ゆっくり、落ち着ける時間に読んでくださいね」のような一言(「詳しくは鑑定書に書きました」は固定で付くので書かない)

【書き方】
- シンプルに。5〜8行程度。情報を詰め込まず、頭にすっと入る量にする
- 日付・月・年・固有名詞は多くても2つまで。細かい数字を並べない
- 短い文をぶつ切りで並べない。「〜なので」「〜ですから」「そのうえで」などでつなぎ、ひと続きの話し言葉にする
- 【必須】改行ルール: 読点(、)のあとで必ず改行する。句点(。)のあとは空行を入れる。読点の間が長すぎる文(25文字超)は、意味の切れ目のいいところで折る
- 深雪の口調: 丁寧で静かな、寄り添う言葉づかい。「視えています」のような言い回しを使ってよい
- 結論は鑑定文の内容に沿って書く。鑑定文にないこと・食い違うことは書かない
- 絵文字は使わない。「──」も使わない。「{名前}様」への呼びかけで始めない(冒頭は固定文が入る)
- 出力は本文だけ。前置き・説明・見出し・記号は付けない

---
"""

OPENING = "{名前}様\n\nおまたせいたしました。"

CLOSING = "鑑定書に詳しく書きました。\nこちらからご覧ください。"

FOOTER = """本鑑定を受けてくださった方
限定の公式LINEになります。
ぜひご登録ください☺️
https://line.me/R/ti/p/%40881vnxcr

お渡しから1週間、
どんな細かいこと、わからないこと
なんでもこちらのDMでお聞きください😊"""



def fmt(text):
    """、で改行 / 。で空行 / 長い行は助詞の切れ目で折る(25文字超)"""
    text = re.sub(r"\s*\n\s*", "", text.strip())
    text = re.sub(r"「[^」]*」", lambda m: m.group(0).replace("、", "\0"), text)
    text = re.sub(r"(、)(?!」)", r"\1\n", text)
    text = re.sub(r"(。)(?!」)", r"\1\n\n", text)
    lines = []
    for ln in text.split("\n"):
        while len(ln) > 25:
            cut = None
            for i in range(12, min(len(ln) - 3, 26)):
                if ln[i] in "をにがはでとてもへ" and ln[i - 1] not in "「" and "「" not in ln[:i] .rsplit("」", 1)[-1]:
                    cut = i + 1
            if cut is None:
                break
            lines.append(ln[:cut]); ln = ln[cut:]
        lines.append(ln)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip().replace("\0", "、")


def load_urls():
    urls = {}
    for line in open(URLS, encoding="utf-8"):
        u = line.strip()
        m = re.search(r"/miyuki/(\d+(?:-\d+)?)_", u)
        if m and u.endswith("/"):
            urls[m.group(1)] = u[u.index("http"):]
    return urls


def main():
    nums = [a for a in sys.argv[1:] if re.fullmatch(r"\d+(-\d+)?", a)]
    if not nums:
        print("使い方: python3 make_watashi.py 1616 1524")
        sys.exit(1)
    urls = load_urls()
    blocks = []
    for num in nums:
        files = sorted(f for f in glob.glob(f"{SRC}/{num}_*/{num}_*_本鑑定文*.txt") if "修正前" not in f)
        if not files:
            print(f"  ⚠ {num}: 本鑑定文txtが見つからないので飛ばします")
            continue
        m = re.match(rf"{num}_(.+?)_本鑑定文", os.path.basename(files[-1]))
        name = m.group(1) if m else ""
        files = files[-1:]
        if num in urls:
            url = urls[num]
        else:
            url = f"{BASE}{num}_{urllib.parse.quote(name + '様')}_{urllib.parse.quote('本式守護鑑定')}/"
        text = open(files[0], encoding="utf-8").read()
        prompt = RULES.replace("{名前}", name) + text
        try:
            out = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                                 stdin=subprocess.DEVNULL, timeout=300).stdout.strip()
        except Exception as e:
            print(f"  ⚠ {num}_{name}: 作成に失敗 ({e})")
            continue
        if len(out) < 100:
            print(f"  ⚠ {num}_{name}: 文章がおかしいので飛ばします → {out!r}")
            continue
        out = fmt(out)
        blocks.append(f"■ {num}_{name}様\n\n{OPENING.replace('{名前}', name)}\n\n{out}\n\n{CLOSING}\n{url}\n\n{FOOTER}")
        print(f"  ✅ {num}_{name}")

    if not blocks:
        print("\n作成できたメッセージがないので、txtはそのままにします。")
        return
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n\n\n========================================\n\n\n".join(blocks) + "\n")
    print(f"\n{len(blocks)} 件 → {OUT}")


if __name__ == "__main__":
    main()
