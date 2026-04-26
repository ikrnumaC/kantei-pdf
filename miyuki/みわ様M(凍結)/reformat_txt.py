#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
txtファイルを20文字ルールで改行調整するスクリプト
"""

import re
import sys
from pathlib import Path


def count_display_length(text):
    """表示上の文字数をカウント（全角1文字、半角0.5文字）"""
    count = 0
    for char in text:
        # 全角文字
        if ord(char) > 127:
            count += 1
        # 半角文字
        else:
            count += 0.5
    return count


def split_by_length(text, max_length=20):
    """
    新ロジック：
    1. 句点（。？！）で必ず改行
    2. 読点（、）で区切られた部分を20文字に近づくように集める
    3. 5文字以下の行ができたら前の行と合体して再分割
    """
    if count_display_length(text) <= max_length:
        return [text]

    # 1. 句点で文を分割
    sentences = re.split(r'([。？！…])', text)
    # 句点を前の文に付ける
    merged_sentences = []
    for i in range(0, len(sentences), 2):
        if i + 1 < len(sentences):
            merged_sentences.append(sentences[i] + sentences[i + 1])
        elif sentences[i]:
            merged_sentences.append(sentences[i])

    # 各文を処理
    all_lines = []
    for sentence in merged_sentences:
        if not sentence.strip():
            continue
        lines = split_sentence_by_comma(sentence, max_length)
        all_lines.extend(lines)

    # 3. 後処理：5文字以下の行を調整
    all_lines = adjust_short_lines(all_lines, max_length)

    return all_lines


def split_sentence_by_comma(sentence, max_length=20):
    """
    読点（、）で区切られた部分を20文字に近づくように集める
    """
    if count_display_length(sentence) <= max_length:
        return [sentence]

    # 読点で分割
    parts = re.split(r'(、)', sentence)
    # 読点を前の部分に付ける
    merged_parts = []
    for i in range(0, len(parts), 2):
        if i + 1 < len(parts):
            merged_parts.append(parts[i] + parts[i + 1])
        elif parts[i]:
            merged_parts.append(parts[i])

    # 読点がない場合は助詞で分割
    if len(merged_parts) <= 1:
        return split_by_particle(sentence, max_length)

    # 20文字に近づくように集める
    lines = []
    current_line = ""

    for part in merged_parts:
        test_line = current_line + part
        if count_display_length(test_line) <= max_length:
            # まだ追加できる
            current_line = test_line
        else:
            # 追加すると超える
            if current_line:
                lines.append(current_line)
            current_line = part

    # 最後の行を追加
    if current_line:
        # 最後の部分が20文字超える場合は助詞で分割
        if count_display_length(current_line) > max_length:
            lines.extend(split_by_particle(current_line, max_length))
        else:
            lines.append(current_line)

    return lines


def split_by_particle(text, max_length=20):
    """
    助詞で分割（読点がない場合のフォールバック）
    """
    if count_display_length(text) <= max_length:
        return [text]

    # 助詞・接続助詞の位置を探す
    particles = ['を', 'に', 'が', 'は', 'も', 'て', 'で', 'と', 'の', 'へ', 'や', 'から', 'まで', 'より']
    split_positions = []

    for particle in particles:
        pos = 0
        while True:
            pos = text.find(particle, pos)
            if pos == -1:
                break

            # 除外パターン：「でも」の「も」
            should_exclude = False
            if particle == 'も' and pos >= 2:
                if text[pos-2:pos] == 'でも':
                    should_exclude = True

            if not should_exclude and pos + len(particle) < len(text):
                split_positions.append((pos + len(particle), text[:pos + len(particle)]))
            pos += len(particle)

    # 位置でソート（後ろから）
    split_positions.sort(key=lambda x: -x[0])

    # max_length以内で最も長い分割点を探す
    best_split = None
    for pos, part in split_positions:
        if count_display_length(part) <= max_length and count_display_length(part) > 0:
            if best_split is None or len(part) > len(best_split[1]):
                best_split = (pos, part)

    if best_split:
        pos = best_split[0]
        first_part = text[:pos]
        rest = text[pos:]
        return [first_part] + split_by_particle(rest, max_length)
    else:
        # どうしても分割できない場合はそのまま
        return [text]


def adjust_short_lines(lines, max_length=20, min_length=5):
    """
    5文字以下の行ができたら前の行と合体して再分割
    """
    if len(lines) <= 1:
        return lines

    adjusted = []
    i = 0

    while i < len(lines):
        current = lines[i]

        # 次の行が5文字以下かチェック
        if i + 1 < len(lines) and count_display_length(lines[i + 1]) <= min_length:
            # 現在の行と次の行を合体
            combined = current + lines[i + 1]

            # 再分割
            if count_display_length(combined) <= max_length:
                # 合体したままでOK
                adjusted.append(combined)
                i += 2
            else:
                # 再分割が必要
                resplit = split_by_particle(combined, max_length)
                adjusted.extend(resplit)
                i += 2
        else:
            adjusted.append(current)
            i += 1

    return adjusted


def reformat_paragraph(paragraph, max_length=20):
    """
    段落を20文字ルールで改行
    """
    # 既存の改行を削除して1行に
    text = paragraph.replace('\n', '')

    if not text.strip():
        return ''

    # 保護すべきパターン（改行してはいけない）
    # 守護神名（括弧付き）、短い行など
    protected_inline = [
        r'(.+?)（[^）]+）',  # 括弧付きの部分は分割しない
    ]

    # 括弧付きの部分を一時的に保護
    protected_parts = {}
    placeholder_text = text
    placeholder_count = 0

    for pattern in protected_inline:
        for match in re.finditer(pattern, text):
            placeholder = f"___PROTECTED_{placeholder_count}___"
            protected_parts[placeholder] = match.group(0)
            placeholder_text = placeholder_text.replace(match.group(0), placeholder, 1)
            placeholder_count += 1

    # 20文字で分割
    if placeholder_text != text:
        # 保護された部分がある場合
        lines = split_by_length(placeholder_text, max_length)
        # 保護された部分を元に戻す
        result_lines = []
        for line in lines:
            for placeholder, original in protected_parts.items():
                line = line.replace(placeholder, original)
            result_lines.append(line)
        return '\n'.join(result_lines)
    else:
        # 通常の分割
        lines = split_by_length(text, max_length)
        return '\n'.join(lines)


def reformat_text(text, max_length=20):
    """
    テキスト全体を20文字ルールで改行調整
    段落（\n\nで区切られた部分）ごとに処理
    """
    # セクション見出しや特別な行を保護
    protected_patterns = [
        r'^【.+】$',           # 【タイトル】
        r'^⛩️.+$',             # ⛩️見出し
        r'^🔮.+$',             # 🔮見出し
        r'^━+$',              # 区切り線
        r'^https?://.+$',     # URL
        r'^・.+$',            # リスト項目
        r'^深[幸雪]$',        # 署名
        r'^▼.+$',             # ▼付き行
    ]

    # 段落ごとに分割
    paragraphs = text.split('\n\n')
    result = []

    for para in paragraphs:
        if not para.strip():
            result.append('')
            continue

        # 保護パターンに一致する場合はそのまま
        is_protected = False
        for pattern in protected_patterns:
            if re.match(pattern, para.strip()):
                is_protected = True
                break

        if is_protected:
            result.append(para)
        else:
            # リフォーマット
            reformatted = reformat_paragraph(para, max_length)
            result.append(reformatted)

    return '\n\n'.join(result)


def reformat_file(input_path, output_path=None, max_length=20):
    """txtファイルを読み込んで改行調整し、保存"""
    # ファイル読み込み
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # リフォーマット
    reformatted = reformat_text(text, max_length)

    # 出力先を決定
    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = input_path_obj.parent / f"{input_path_obj.stem}_formatted{input_path_obj.suffix}"

    # 保存
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(reformatted)

    print(f"✅ 改行調整完了: {output_path}")
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使い方: python reformat_txt.py <txtファイルパス> [出力ファイルパス] [最大文字数]")
        print("例: python reformat_txt.py input.txt output.txt 20")
        print("例: python reformat_txt.py input.txt  # 自動で input_formatted.txt が作成される")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    max_len = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    reformat_file(input_file, output_file, max_len)
