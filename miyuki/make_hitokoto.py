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
# --- クラウドのClaudeから回すとき用（ふだんの python3 make_hitokoto.py は API を呼ぶ）---
#   HITOKOTO_EXPORT=フォルダ … claude を呼ばず、1件ずつの依頼文を フォルダ/連番.txt に書き出すだけ（CSVは変えない）
#   HITOKOTO_IMPORT=フォルダ … claude を呼ばず、フォルダ/連番.out（2行）を答えとして読み、チェックしてCSVを作る
EXPORT = os.environ.get("HITOKOTO_EXPORT", "")
IMPORT = os.environ.get("HITOKOTO_IMPORT", "")
#   HITOKOTO_REPO=フォルダ … kantei の写しを置いた場所で動かす（クラウド側の Bash から API を呼ぶとき用）
if os.environ.get("HITOKOTO_REPO"):
    REPO = os.environ["HITOKOTO_REPO"]
if not os.path.isdir(REPO):
    REPO = os.path.expanduser("~/mnt/kantei")

# --- 一言はAPIで作る（2026-11-27〜。サブスクの週間枠を使わないため）---
#   APIキー: 環境変数 ANTHROPIC_API_KEY、なければ kantei/.env（本鑑定APIと同じ）
#   HITOKOTO_MODEL=モデル名 … 使うモデルを変える（既定 claude-sonnet-5-5）
#   HITOKOTO_USE_CLI=1 … 前のやり方（claude -p）に戻す
MODEL = os.environ.get("HITOKOTO_MODEL", "claude-sonnet-5-5")
USE_CLI = os.environ.get("HITOKOTO_USE_CLI", "") == "1"
API_USAGE = {"in": 0, "out": 0, "calls": 0}

def api_key():
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"].strip()
    p = os.path.join(REPO, ".env")
    if os.path.isfile(p):
        for line in open(p, encoding="utf-8"):
            if line.strip().startswith("ANTHROPIC_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("APIキーが見つかりません（kantei/.env に ANTHROPIC_API_KEY=... を入れてください）")

def ask_api(prompt):
    import json, time, urllib.request, urllib.error
    try:
        import ssl
        if os.environ.get("SSL_CERT_FILE"):   # クラウド側の Bash はプロキシの証明書を使う
            ctx = ssl.create_default_context(cafile=os.environ["SSL_CERT_FILE"])
        else:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ctx = None
    # 考える分も出力枠に入るので max_tokens は大きめに（400 だと本文が空で返った）。
    # 考えさせないと、かなの「1行32字以内」を守れず形チェックで落ちる（2026-11-27 に試した）
    body = {"model": MODEL, "max_tokens": 6000,
            "messages": [{"role": "user", "content": prompt}]}
    last = ""
    for attempt in range(3):
        req = urllib.request.Request("https://api.anthropic.com/v1/messages",
                                     data=json.dumps(body).encode("utf-8"),
                                     headers={"x-api-key": api_key(), "anthropic-version": "2023-06-01",
                                              "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300, context=ctx) as r:
                d = json.loads(r.read().decode("utf-8"))
            u = d.get("usage", {})
            API_USAGE["in"] += u.get("input_tokens", 0)
            API_USAGE["out"] += u.get("output_tokens", 0)
            API_USAGE["calls"] += 1
            return "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}"
            if e.code not in (429, 500, 502, 503, 529):
                break
        except Exception as e:
            last = repr(e)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"APIの呼び出しに失敗: {last}")

def ask(prompt, num):
    if IMPORT:
        p = os.path.join(IMPORT, f"{num}.out")
        return open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    if USE_CLI:
        return subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, timeout=300).stdout
    return ask_api(prompt)
URLS = f"{REPO}/miyuki/miyukiurl.txt"
CSV = f"{REPO}/miyuki/miyuki_hitokoto.csv"
FREE = f"{REPO}/無料鑑定/深雪"

RULES = """下の深雪の無料鑑定文を読んで、お客様に送るLINEメッセージに差し込む「一言」を2行だけ作ってください。

【書き方】
- 1行目: 「{名前}様の」に続けて、相談者自身の言葉を「」で短く引く(【相談内容】の言葉から)。最後は「〜を視ていく中で」などで2行目につなぐ
- 2行目: 名前は入れない(1行目で名前を出したので繰り返さない。「{名前}様を守る」ではなく「あなたを守る」)。鑑定文に書いてある守護神の名前(例: 火産霊神)を必ず入れ、「あなたを守る○○神が、」の形にする(「神様が」と一般名で済ませない。「〜神」は読みやすいよう鑑定文の表記のままで、読み仮名は付けない)。続きは鑑定文に実際に書いてあることの予告(姿を見せてくれた、未来の姿を視せてくれた など)。答え(できる・いつ等)は書かない
- 「驚くような」は、鑑定文の中身が本当に意外な時だけ使う
- 1行は30文字前後まで。深雪の丁寧で静かな言葉づかい
- 出力は2行だけ。前置き・説明・番号・記号は付けない

例:
きゅあ様の「あの方と、もう一度」という想いを視ていく中で
あなたを守る火産霊神が、はっきりと姿を見せてくれました。

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
        with open(CSV, encoding="utf-8-sig", newline="") as f:
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
        if EXPORT:
            os.makedirs(EXPORT, exist_ok=True)
            open(os.path.join(EXPORT, f"{num}.txt"), "w", encoding="utf-8").write(prompt)
            print(f"  📝 {num}_{name}: 依頼文を書き出し")
            continue
        try:
            out = ask(prompt, num)
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
    with open(CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["URL", "一言1", "一言2"])
        w.writerows(new_rows)
    print(f"\n{len(new_rows)} 件(今回の新規分のみ) → {CSV}")
    print("スプシの右側(H〜J列)に、このCSVを貼ってください。")

if __name__ == "__main__":
    main()
    if API_USAGE["calls"]:
        print(f"API（{MODEL}）: {API_USAGE['calls']}回 入力{API_USAGE['in']} 出力{API_USAGE['out']} トークン")
