#!/usr/bin/env python3
# ============================================================
# 深雪 無料鑑定 送付メッセージ用「一言」作成スクリプト
#
# 使い方:
#   python3 make_hitokoto.py          … 一言ファイルにまだ無いURLだけ作る
#   python3 make_hitokoto.py 1641     … 初回だけ: 1641番以降を対象にする
#
# 動作:
#   - miyukiurl.txt の無料鑑定URL(…様M/)のうち、miyuki_hitokoto.csv の最大連番より後のものを探す
#   - 対象は「一言ファイルにある最大の連番より後」(初回は引数の番号以降)
#   - 1件ずつ無料鑑定の文章を claude に読ませて、一言を2行作る
#   - miyuki_hitokoto.csv (URL, 一言1, 一言2) を今回の新規分だけに入れ替える(前回分は消える)
#   → スプシの右側(例: H〜J列)に、このCSVを貼る
# ============================================================
import csv, glob, os, re, subprocess, sys, urllib.parse

REPO = "/Users/miura/Documents/GitHub/kantei"
URLS = f"{REPO}/miyuki/miyukiurl.txt"
CSV = f"{REPO}/miyuki/miyuki_hitokoto.csv"
FREE = f"{REPO}/無料鑑定/深雪"

RULES = """下の深雪の無料鑑定文を読んで、お客様に送るLINEメッセージに差し込む「一言」を2行だけ作ってください。

【書き方】
- 1行目: 「{名前}様の」に続けて、相談者自身の言葉を「」で短く引く(【相談内容】の言葉から)。最後は「〜を視ていく中で」などで2行目につなぐ
- 2行目: 名前は入れない(1行目で名前を出したので繰り返さない。「{名前}様を守る」ではなく「あなたを守る」)。鑑定文に実際に書いてあることの予告(守護神が姿を見せた、未来の姿が視えた など)。答え(できる・いつ等)は書かない
- 「驚くような」は、鑑定文の中身が本当に意外な時だけ使う
- 1行は30文字前後まで。深雪の丁寧で静かな言葉づかい
- 出力は2行だけ。前置き・説明・番号・記号は付けない

例:
きゅあ様の「あの方と、もう一度」という想いを視ていく中で
あなたを守る神様が、はっきりと姿を見せてくれました。

---
"""

def parse(url):
    m = re.search(r"/miyuki/([^/]+)/?$", url.strip())
    if not m:
        return None
    key = urllib.parse.unquote(m.group(1))
    m2 = re.match(r"^(\d+)_(.+)様M$", key)
    if not m2:
        return None
    return int(m2.group(1)), m2.group(2)

def main():
    rows = []
    if os.path.exists(CSV):
        with open(CSV, encoding="utf-8", newline="") as f:
            rows = [r for r in csv.reader(f) if r]
        if rows and rows[0][0] == "URL":
            rows = rows[1:]
    done = {r[0] for r in rows}
    done_nums = [parse(u)[0] for u in done if parse(u)]

    if len(sys.argv) > 1:
        start = int(sys.argv[1])
    elif done_nums:
        start = max(done_nums) + 1
    else:
        print("❌ 初回は開始番号を指定してください 例: python3 make_hitokoto.py 1641")
        sys.exit(1)

    targets = []
    with open(URLS, encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            p = parse(url) if url else None
            if p and p[0] >= start and url not in done:
                targets.append((p[0], p[1], url))
    targets.sort()
    if not targets:
        print("新しく作る一言はありません。")
        return

    print(f"対象 {len(targets)} 件: " + ", ".join(f"{n}_{nm}" for n, nm, _ in targets))
    new_rows = []
    for num, name, url in targets:
        files = glob.glob(f"{FREE}/{num}_*_深雪.txt")
        if not files:
            print(f"  ⚠ {num}_{name}: 無料鑑定ファイルが見つからないので飛ばします")
            continue
        text = open(files[0], encoding="utf-8").read()
        prompt = RULES.replace("{名前}", name) + text
        try:
            out = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                                 stdin=subprocess.DEVNULL, timeout=300).stdout
        except Exception as e:
            print(f"  ⚠ {num}_{name}: 作成に失敗 ({e})")
            continue
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        if len(lines) == 1 and "／" in lines[0]:
            lines = [x.strip() for x in lines[0].split("／", 1)]
        if len(lines) < 2:
            print(f"  ⚠ {num}_{name}: 一言の形がおかしいので飛ばします → {out!r}")
            continue
        new_rows.append([url, lines[-2], lines[-1]])
        print(f"  ✅ {num}_{name}: {lines[-2]} / {lines[-1]}")

    if not new_rows:
        print("\n作成できた一言がないので、CSVはそのままにします。")
        return
    # 前回分は消して、今回の新規分だけを残す(最大番号は上で読み取り済み)
    new_rows.sort(key=lambda r: parse(r[0])[0] if parse(r[0]) else 0)
    with open(CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["URL", "一言1", "一言2"])
        w.writerows(new_rows)
    print(f"\n{len(new_rows)} 件(今回の新規分のみ) → {CSV}")
    print("スプシの右側(H〜J列)に、このCSVを貼ってください。")

if __name__ == "__main__":
    main()
