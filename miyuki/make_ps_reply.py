#!/usr/bin/env python3
"""深雪のPS文(txt)から、PSページを渡すときの返信文を作る。

使い方（Claudeが実行する。手では動かさない）:
    python3 miyuki/make_ps_reply.py 有料鑑定/深雪/1836_おりひめ様_本式守護鑑定/1836_おりひめ_PS.txt [--force]

PS文から名前・石3つ・守護神・合図の言葉・連番を拾い、同じフォルダに 連番_名前_返信.txt を作る。
すでにあるときは上書きしない（--force で上書き）。お客様の質問への回答など個別の返信は、
このスクリプトの範囲外。必要なら出来上がったtxtの前半に足す。
"""
import re
import sys
import urllib.parse
from pathlib import Path

BASE_URL = "https://kantei-pdf.pages.dev/miyuki/"

TEMPLATE = """{name}様

こんにちは。
「詳細希望」のご連絡、ありがとうございます。

{name}様の命の流れを視て選んだ
{stones}。
この3つの石を、{guardian}の守護とともに
ひとつのページにまとめました。

{signal}
手首の石にそっと触れて
その合図を思い出すための石です。

価格は29,800円です。
{name}様と響き合う石を
一粒ずつ手で編んでお作りします。

詳細はこちらをご覧ください。

{url}

また気になることがあれば
いつでもメッセージくださいね。

深雪
"""


def main():
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv
    if len(args) != 1:
        sys.exit(__doc__)
    src = Path(args[0]).resolve()
    text = src.read_text(encoding="utf-8")

    m = re.match(r"(\d+)_(.+)_PS\.txt$", src.name)
    if not m:
        sys.exit(f"ファイル名が 連番_名前_PS.txt の形ではありません: {src.name}")
    num, name = m.groups()

    errors = []
    sm = re.search(r"^(.+?)。\nこの3つを", text, re.M)
    gm = re.search(r"^(\S+?（[^）]+）)が\n深く共鳴する3つの石", text, re.M)
    cm = re.search(r"身につけていくうちに、\n「([^」]+)」", text)
    if not sm:
        errors.append("石3つの行（「A・B・C。この3つを…」）が見つかりません")
    if not gm:
        errors.append("守護神名（「◯◯（読み）が深く共鳴する3つの石」）が見つかりません")
    if not cm:
        errors.append("合図の言葉（「身につけていくうちに、」の次の行の「◯◯」）が見つかりません")
    if errors:
        sys.exit("エラー:\n  " + "\n  ".join(errors))

    guardian = re.sub(r"（[^）]+）", "", gm.group(1))  # 返信文では読み仮名を省く
    url = BASE_URL + urllib.parse.quote(f"{num}_{name}様PS") + "/"
    out = TEMPLATE.format(name=name, stones=sm.group(1), guardian=guardian,
                          signal=f"「{cm.group(1)}」。", url=url)

    dst = src.with_name(f"{num}_{name}_返信.txt")
    if dst.exists() and not force:
        sys.exit(f"{dst.name} はすでにあります（上書きは --force）")
    dst.write_text(out, encoding="utf-8")
    print(f"作成: {dst}\n")
    print(out)


if __name__ == "__main__":
    main()
