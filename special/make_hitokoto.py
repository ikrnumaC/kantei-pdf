#!/usr/bin/env python3
# ============================================================
# かな 無料鑑定 送付メッセージ用「一言」作成スクリプト (special)
#
# 使い方:
#   python3 make_hitokoto.py          … 一言ファイルにまだ無いURLだけ作る
#   python3 make_hitokoto.py 1774     … 初回だけ: 1774番以降を対象にする
#
# 動作:
#   - urls.txt の無料鑑定URL(…/special/連番_名前様/)のうち、kana_hitokoto.csv にまだ無いものを探す
#   - 対象は「一言ファイルにある最大の連番より後」(初回は引数の番号以降)
#   - 1件ずつ 無料鑑定/かな の文章を claude に読ませて、一言を2行作る
#   - 前回までのCSVから最大の連番を取得したうえで、CSVを今回作った分だけに置き換える
#   → スプシの右側に、このCSVを丸ごと貼り直す
# ============================================================
import csv, glob, os, re, subprocess, sys, urllib.parse

REPO = "/Users/miura/Documents/GitHub/kantei"
URLS = f"{REPO}/special/urls.txt"
CSV = f"{REPO}/special/kana_hitokoto.csv"
FREE = f"{REPO}/無料鑑定/かな"

ADVERBS = ["丁寧に", "真剣に", "心を込めて", "じっくり", "一つひとつ", "まっすぐに", "静かに", "しっかり"]

RULES = """下のかなの無料鑑定文を読んで、お客様に送るLINEメッセージの中に差し込む「一言」を2行だけ作ってください。
このメッセージは「鑑定書ができました。…あなたのオーラが一体何色なのか、どうすれば望む未来が手に入れられるのか…」という文面の前後に入ります。読んだ人が「早く読みたい」とわくわくすることが一番の目的です。

【書き方】
- 文体は必ず丁寧語(です・ます)。ため口(〜だよ、〜な、〜ね)は使わない。やわらかく、あたたかい敬語
- お客様のことは基本「あなた」。名前で呼んでもよい(鑑定文の呼び方に合わせる。例: 志津恵さん)が、無理に入れなくてよい。相手の名前(Mさん等)は出さず、「彼」「あの方」などで言う
- 1行目と2行目は、改行を挟んで1つの文として自然につながること。1行目は「〜を{副詞}視ていく中で」「〜について{副詞}視ていたら」のように接続の形(ので・中で・たら・ながら等)で終え、2行目がその続きになる。両方とも「〜ました。」で言い切る形にしない(ぶっきらぼうになる)
- 「〜中で」「〜ので」「〜たら」などの接続は1行目の中で重ねない(例: 「繰り返す中で、〜視ていく中で、」は不可)。1行の中に接続の形は1回だけにして、前半は「〜を繰り返しながら、」「〜というお気持ちを」のように言い換える
- 視る時の副詞は「{副詞}」を使う(「ゆっくり」は使わない)
- 1行目: 【ご相談内容】の内容を、自然な日本語で文に溶かして入れる。「」は付けても付けなくてもよい。付ける時は原文のままの言葉だけ。引用が文や疑問の形なら「のこと」ではなく「という想い」「というお気持ち」等で受ける。「言葉を視ていたら」とは書かない
- 2行目: 1行目の続きとして、次の4種類の中から鑑定文に実際に書いてあるものを1つだけ選び、具体的に予告する。
  (a) あなたのいいところ・持っている力 (b) あなたの今の状況 (c) 彼(相手)のオーラ (d) 彼(相手)の今の状況
  (c)(d)は、鑑定文に相手が出てくる時だけ使う。相手がいない鑑定文では(a)(b)から選ぶ
  これからの流れ・方法・サイン・時期・道筋・アドバイス・対処法など、無料鑑定に書いていないことは絶対に予告しない
  「歩み」「道のり」のような抽象語は使わず、鑑定文の中の具体的な内容(何についてか)が分かる言い方にする
  オーラの色そのものは書かない。答え(できる・いつ等)も書かない
  例: 「彼の今のお気持ちについて〜」「あなたが自然に持っている〇〇な力について〜」
- 乱れ・崩れ・心配・気になる・不安につながる言葉は使わない
- 「縁の流れ」「はっきり視えた」「姿を見せてくれた」のような誰にでも使える定型句は使わない。鑑定文にない言葉は使わない
- 「驚いた」「驚くような」とは書かない
- 1行は25文字前後まで、長くても30文字
- 2行目の文末は「〜についてお伝えしたいことが見つかりました。」「〜が視えてきました。」を基本にして(「〜について書きました。」は使わない。「視」の字を使う)、毎回変える(「お伝えしたいことがありました」「お伝えしたいことがあります」は使わない)
- 語尾や言い回しは毎回変える
- 相手の名前や「彼」「Mさん」などの人物名は2行目に出さない。主語は「あなた」か、省略する
- 時期・結果・行動の指示(いつ連絡が来る、こう動く等)をにおわせる言い方は避け、「〜が視えてきました」と、テーマ名だけを予告する(「〜について書きました」ではなく「〜が視えてきました」)
- 出力は2行だけ。前置き・補足・注釈・かっこ書き・番号・記号は絶対に付けない

形の例(中身は鑑定文ごとに変えること):
〇〇というお気持ちをゆっくり視ていく中で、
△△についてお伝えしたいことが見つかりました。

---
"""

def parse(url):
    m = re.search(r"/special/([^/]+)/?$", url.strip())
    if not m:
        return None
    key = urllib.parse.unquote(m.group(1))
    m2 = re.match(r"^(\d+)_(.+)様$", key)
    if not m2:
        return None
    return int(m2.group(1)), m2.group(2)

def break_at_comma(t):
    """「、」のあとで改行する(文末の「、」は除く・何度かけても同じ結果)"""
    return re.sub(r"、(?!\n)(?=.)", "、\n", t)

def is_valid(lines, text):
    """2行ちょうど・かっこ書きなし・1行目が「。」で言い切られていない、を満たすか"""
    if len(lines) != 2 or any(re.search(r"[()（）]|補足|注", l) for l in lines):
        return False
    if re.search(r"、、|ゆっくり|についても", "".join(lines)) or lines[0].count("中で") > 1:
        return False
    if lines[0].endswith("。") or not lines[1].endswith("。"):
        return False
    q = re.search(r"「([^」]+)」", lines[0])
    if q and q.group(1) not in text.split("霊視した瞬間")[0]:
        return False
    return True

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
        print("❌ 初回は開始番号を指定してください 例: python3 make_hitokoto.py 1774")
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
    new = 0
    new_rows = []
    for num, name, url in targets:
        files = glob.glob(f"{FREE}/{num}_*_かな.txt")
        if not files:
            print(f"  ⚠ {num}_{name}: 無料鑑定ファイルが見つからないので飛ばします")
            continue
        text = open(files[0], encoding="utf-8").read()
        prompt = RULES.replace("{副詞}", ADVERBS[num % len(ADVERBS)]).replace("{名前}", name) + text
        lines, out = None, ""
        for _ in range(3):
            try:
                out = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                                     stdin=subprocess.DEVNULL, timeout=300).stdout
            except Exception as e:
                print(f"  ⚠ {num}_{name}: 作成に失敗 ({e})")
                continue
            lines = [l.strip() for l in out.splitlines() if l.strip()]
            if len(lines) == 1 and "／" in lines[0]:
                lines = [x.strip() for x in lines[0].split("／", 1)]
            cands = [lines, lines[-2:]]
            lines = next((c for c in cands if is_valid(c, text)), None)
            if lines:
                break
        if not lines:
            print(f"  ⚠ {num}_{name}: 一言の形がおかしいので飛ばします → {out!r}")
            continue
        new_rows.append([url, break_at_comma(lines[-2]), break_at_comma(lines[-1])])
        new += 1
        print(f"  ✅ {num}_{name}: {lines[-2]} / {lines[-1]}")

    if not new_rows:
        print("\n追加できた一言がないので、CSVは変更しません。")
        return
    rows = sorted(new_rows, key=lambda r: parse(r[0])[0])
    with open(CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["URL", "一言1", "一言2"])
        w.writerows(rows)
    print(f"\n{new} 件で置き換えました → {CSV}")
    print("スプシの右側に、このCSVを丸ごと貼り直してください。")

if __name__ == "__main__":
    main()
