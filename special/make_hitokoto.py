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
- 2行目: 1行目の続きとして、鑑定文の中で実際に言い切っている「結論」に触れる。「最初にお伝えします」「二人の行方」「今の状況」のあたりにある、ご相談内容への答えそのもの、または相手(彼・彼女)の今の状況を、鑑定文の言葉に沿って具体的に1つだけ書く
  例: 「縁がまだ終わっていないことが視えてきました。」「相手の方があなたを思い浮かべた時の変化が視えてきました。」「この恋が発展していく可能性を持っていることが視えてきました。」(中身は必ず鑑定文ごとに変える。例の言葉をそのまま使わない)
  言葉は必ず鑑定文の中でかなが実際に使っている表現(「まだ終わっていません」「発展していく可能性を持っています」「〜の間にいます」など)から取る。「道」「道筋」「形に整える」のように、鑑定文にない概念語・言い換えは使わない。鑑定文の言い回しを、2行目の語尾に合うよう最小限だけ変えて使う
  鑑定文の結論の文は長いので、そのまま写さず、核になる部分だけを30文字以内に短く切り出す(例: 「彼との縁は唯一無二の関係に育てていく道があります」→「この縁を育てていく道が視えてきました。」)。切り出す時も、相手の名前(Aさん等)は「この縁」「お相手」に置き換える
  「あなたが自然に持っている〇〇の力について」「〜について」だけで中身が分からない、誰にでも当てはまる書き方は禁止。読んだ人が「結論が書いてある」と分かること
  時期・きっかけ・近づき方・オーラの整え方・本鑑定でお伝えする4項目の中身(お相手の本当の気持ち、もう一つの重要な問題など)は書かない。無料鑑定でまだ明かしていないことは絶対に書かない
  オーラの色そのものは書かない
- 乱れ・崩れ・心配・気になる・不安につながる言葉は使わない
- 「縁の流れ」「はっきり視えた」「姿を見せてくれた」のような誰にでも使える定型句は使わない。鑑定文にない言葉は使わない
- 「驚いた」「驚くような」とは書かない
- 1行は25文字前後まで、長くても30文字
- 2行目の文末は「〜が視えてきました。」「〜が視えています。」「〜を視つけました。」などから毎回変える(「〜について書きました。」「お伝えしたいことが見つかりました」「お伝えしたいことがありました」は使わない。「視」の字を使う)
- 語尾や言い回しは毎回変える
- 相手の名前(A・Mさん等のイニシャルも含む)は1行目にも2行目にも出さない。相手のことは鑑定文の呼び方に合わせて「彼」「彼女」「お相手の方」と言う
- 副詞は{副詞}だけを使い、「そっと丁寧に」のように他の副詞を重ねない。「気持ち」という語は1行目で1回だけ(「気持ちを…というお気持ちを」のような重複は不可)
- 時期・行動の指示(いつ連絡が来る、こう動く等)をにおわせる言い方は避ける
- 出力は2行だけ。前置き・補足・注釈・かっこ書き・番号・記号は絶対に付けない

形の例(中身は鑑定文ごとに変えること):
〇〇というお気持ちを{副詞}視ていく中で、
△△が視えてきました。

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
    """30文字を超える行だけ「、」のあとで改行する(文末の「、」は除く・何度かけても同じ結果)"""
    if len(t) <= 30:
        return t
    return re.sub(r"、(?!\n)(?=.)", "、\n", t)

def is_valid(lines, text, adv="", recent=()):
    """2行ちょうど・かっこ書きなし・1行目が「。」で言い切られていない、を満たすか"""
    if len(lines) != 2 or any(re.search(r"[()（）]|補足|注", l) for l in lines):
        return False
    if re.search(r"、、|ゆっくり|についても", "".join(lines)) or lines[0].count("中で") > 1:
        return False
    if lines[0].endswith("。") or not lines[1].endswith("。"):
        return False
    if any(len(l) > 32 for l in lines):
        return False
    if re.search(r"[A-ZＡ-Ｚa-z]さん|[A-ZＡ-Ｚ]様", "".join(lines)):
        return False
    if lines[0].count("気持ち") > 1 or re.search(r"(そっと|優しく|穏やかに)\s*(" + "|".join(ADVERBS) + ")", lines[0]):
        return False
    if adv and adv not in lines[0]:
        return False
    if re.search(r"自然に持っている|力について|お伝えしたいこと", lines[1]) or lines[1] in recent:
        return False
    body = re.sub(r"(が|を|も)?(視えてきました|視えています|視つけました)。$", "", lines[1])
    body = re.sub(r"(こと|の|という)$", "", body)
    if len(body) >= 6 and not any(body[i:i+6] in text for i in range(len(body) - 5)):
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
    recent = []
    for num, name, url in targets:
        files = glob.glob(f"{FREE}/{num}_*_かな.txt")
        if not files:
            print(f"  ⚠ {num}_{name}: 無料鑑定ファイルが見つからないので飛ばします")
            continue
        text = open(files[0], encoding="utf-8").read()
        adv = ADVERBS[num % len(ADVERBS)]
        avoid = ("【直近の一言(この言い回しと似せない)】\n" + "\n".join(recent[-4:]) + "\n\n---\n") if recent else ""
        prompt = RULES.replace("{副詞}", adv).replace("{名前}", name) + avoid + text
        lines, out = None, ""
        for _ in range(5):
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
            lines = next((c for c in cands if is_valid(c, text, adv, recent)), None)
            if lines:
                break
        if not lines:
            print(f"  ⚠ {num}_{name}: 一言の形がおかしいので飛ばします → {out!r}")
            continue
        recent.append(lines[-1])
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
