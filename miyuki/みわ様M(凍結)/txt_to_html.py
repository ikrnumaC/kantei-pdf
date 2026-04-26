#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
守護神鑑定書 txt → HTML 変換スクリプト
"""

import re
import sys
from pathlib import Path


def extract_name(text):
    """名前を抽出（例: みわ様、→ みわ）"""
    match = re.search(r'([ぁ-んァ-ヶー一-龠々]+)様、', text)
    if match:
        return match.group(1)
    return None


def extract_guardian_info(text):
    """守護神名と説明を抽出"""
    # 守護神名の抽出（例: 豊玉姫（とよたまひめ）。）
    # 改行があってもなくても対応
    match = re.search(r'あなたを守っているのは、\s*(.+?)。', text)
    if match:
        guardian_full = match.group(1)
        # 読み仮名を含む場合の処理
        if '（' in guardian_full and '）' in guardian_full:
            guardian_name = guardian_full.split('（')[0]
            guardian_reading = guardian_full.split('（')[1].split('）')[0]
        else:
            guardian_name = guardian_full
            guardian_reading = ''

        # 守護神の説明を抽出
        desc_match = re.search(r'あなたを守っているのは、\s*.+?\。\s*(.+?)(?:\n\n|$)', text, re.DOTALL)
        if desc_match:
            guardian_desc = desc_match.group(1).strip().split('\n')[0]
        else:
            guardian_desc = ''

        return {
            'name': guardian_name,
            'reading': guardian_reading,
            'full': guardian_full,
            'description': guardian_desc
        }
    return None


def extract_aura_info(text):
    """オーラ情報を抽出"""
    match = re.search(r'あなたのオーラは、\s*(.+?)(?:\n\n|$)', text, re.DOTALL)
    if match:
        aura_text = match.group(1).strip()
        # 最初の段落のみ取得（\n\nまで）
        if '\n\n' in aura_text:
            aura_text = aura_text.split('\n\n')[0]
        return aura_text
    return None


def extract_essence(text):
    """本質を抽出"""
    match = re.search(r'それがあなたの本質です。', text)
    if match:
        # 本質の前の2-3行を取得
        lines_before = text[:match.start()].split('\n')
        essence_lines = [line for line in lines_before[-3:] if line.strip()]
        return '\n'.join(essence_lines)
    return None


def split_sections(text):
    """⛩️でセクションを分割"""
    # ━━━━の後から開始
    main_text = text.split('━━━━━━━━━━━━━━━━')[1] if '━━━━' in text else text

    sections = {
        'aura': '',
        'guardian_type': '',
        'essence': '',
        'flow_bad': '',
        'troubles': '',
        'why_bad': '',
        'two_paths': '',
        'method': '',
        'four_items': [],
        'cta': '',
        'closing': ''
    }

    # イントロ部分は別途抽出（オーラ、守護神タイプ、本質の部分）
    # 「あなたのオーラは」から「その原因をお伝えします」まで
    intro_match = re.search(r'あなたのオーラは、\n(.+?)その原因をお伝えします。', main_text, re.DOTALL)
    if intro_match:
        intro_text = intro_match.group(1).strip()

        # オーラ部分
        aura_match = re.search(r'^(.+?)\n\n', intro_text, re.DOTALL)
        if aura_match:
            sections['aura'] = aura_match.group(1).strip()

        # 守護神タイプと本質
        rest = intro_text[aura_match.end():] if aura_match else intro_text
        parts = rest.split('\n\n')
        if len(parts) >= 2:
            sections['guardian_type'] = parts[0].strip()
            sections['essence'] = parts[1].strip()

        # 「これほど強い守護神に〜」の部分
        flow_match = re.search(r'(これほど強い守護神に.+)', intro_text, re.DOTALL)
        if flow_match:
            sections['flow_bad'] = flow_match.group(1).strip()

    # お悩みについて
    troubles_match = re.search(r'⛩️お悩みについて\n\n(.+?)⛩️', main_text, re.DOTALL)
    if troubles_match:
        sections['troubles'] = troubles_match.group(1).strip()

    # なぜ今、悪いものを引き寄せているのか
    why_match = re.search(r'⛩️なぜ今、悪いものを引き寄せているのか\n\n(.+?)⛩️二つの道', main_text, re.DOTALL)
    if why_match:
        sections['why_bad'] = why_match.group(1).strip()

    # 二つの道
    paths_match = re.search(r'⛩️二つの道\n\n(.+?)⛩️守護の方法', main_text, re.DOTALL)
    if paths_match:
        sections['two_paths'] = paths_match.group(1).strip()

    # 守護の方法
    method_match = re.search(r'⛩️守護の方法\n\n(.+?)🔮', main_text, re.DOTALL)
    if method_match:
        sections['method'] = method_match.group(1).strip()

    # 4つの項目
    items_match = re.search(r'🔮本格守護鑑定でお伝えすること\n\n(.+?)【運命が動く24時間】', main_text, re.DOTALL)
    if items_match:
        items_text = items_match.group(1).strip()
        # ⛩️で分割
        items = re.split(r'⛩️\s*', items_text)
        for item in items:
            if item.strip():
                sections['four_items'].append(item.strip())

    # CTA（【運命が動く24時間】から最後の━までか、最後のhttps://の後まで）
    cta_match = re.search(r'【運命が動く24時間】\n\n(.+?)(?:━━━━|$)', main_text, re.DOTALL)
    if cta_match:
        cta_text = cta_match.group(1).strip()
        # ━より前で切る
        if '━━━━' in cta_text:
            cta_text = cta_text.split('━━━━')[0].strip()
        sections['cta'] = cta_text

    # クロージング（最後の━の後から最後まで）
    # 元のテキスト全体から抽出（main_textではなくtext全体）
    closing_match = re.search(r'━━━━━━━━━━━━━━━━\n\n(.+)$', text, re.DOTALL)
    if closing_match:
        # 最後の━の後が複数ある場合は最後のを取得
        all_closing = closing_match.group(1).strip()
        # 複数の━で分割されている場合、最後のセクションを取得
        if '━━━━━━━━━━━━━━━━' in all_closing:
            # さらに━がある場合はその後を取得
            sections['closing'] = all_closing.split('━━━━━━━━━━━━━━━━')[-1].strip()
        else:
            sections['closing'] = all_closing

    return sections


def text_to_html_paragraph(text, style=''):
    """テキストを<p>タグに変換（改行は<br>に）"""
    paragraphs = text.split('\n\n')
    html_parts = []

    for para in paragraphs:
        if not para.strip():
            continue
        # 段落内の改行を<br>に変換
        content = para.replace('\n', '<br>')
        if style:
            html_parts.append(f'<p style="{style}">{content}</p>')
        else:
            html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    return '\n            '.join(html_parts)


def extract_list_items(text):
    """・で始まるリスト項目を抽出"""
    lines = text.split('\n')
    items = []
    for line in lines:
        if line.strip().startswith('・'):
            items.append(line.strip()[1:].strip())
    return items


def generate_html(txt_path, output_dir=None):
    """txtファイルからHTMLを生成"""

    # txtファイルを読み込み
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 情報を抽出
    name = extract_name(text)
    if not name:
        print("エラー: 名前を抽出できませんでした")
        return

    guardian = extract_guardian_info(text)
    if not guardian:
        print("エラー: 守護神情報を抽出できませんでした")
        return

    aura = extract_aura_info(text)
    essence = extract_essence(text)
    sections = split_sections(text)

    # 画像パスを設定
    guardian_image = f"../鑑定画像/{guardian['name']}.png"

    print(f"📝 変換中: {name}様 - 守護神: {guardian['name']}")

    # HTMLテンプレートを生成
    html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}様　守護神鑑定書</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'YuMincho', serif;
            background: linear-gradient(135deg, #1a1a3e 0%, #0f0f2e 50%, #1a1a3e 100%);
            color: #e8e8f0;
            line-height: 1.8;
            padding: 20px;
            min-height: 100vh;
            font-size: 17px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: rgba(15, 15, 46, 0.7);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(100, 100, 200, 0.2),
                        inset 0 0 60px rgba(100, 100, 200, 0.05);
            border: 1px solid rgba(200, 200, 255, 0.1);
        }}

        h1 {{
            text-align: center;
            color: #a8b8ff;
            font-size: 2em;
            margin-bottom: 30px;
            text-shadow: 0 0 20px rgba(168, 184, 255, 0.5);
            letter-spacing: 0.1em;
        }}

        h2 {{
            color: #c8d0ff;
            font-size: 1.5em;
            margin: 40px 0 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(168, 184, 255, 0.3);
            letter-spacing: 0.05em;
        }}

        .oracle-message {{
            background: linear-gradient(135deg, rgba(60, 60, 120, 0.3), rgba(40, 40, 100, 0.3));
            border: 2px solid rgba(168, 184, 255, 0.3);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 4px 20px rgba(100, 100, 200, 0.2);
            position: relative;
        }}

        .oracle-message::before {{
            content: '';
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 30px;
            background: #1a1a3e;
            padding: 0 15px;
        }}

        .guardian-image {{
            max-width: 400px;
            width: 100%;
            height: auto;
            margin: 30px auto;
            display: block;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(168, 184, 255, 0.3);
        }}

        .oracle-message p {{
            margin: 15px 0;
            text-align: center;
            font-size: 1.1em;
        }}

        .section {{
            margin: 30px 0;
            padding: 20px;
            background: rgba(30, 30, 70, 0.3);
            border-radius: 10px;
            text-align: center;
        }}

        .emoji-header {{
            font-size: 1.8em;
            margin: 40px 0 20px;
            color: #c8d0ff;
            text-align: left;
        }}

        .guardian {{
            text-align: center;
            font-size: 1.3em;
            color: #a8b8ff;
            margin: 20px 0;
            padding: 20px;
            background: rgba(168, 184, 255, 0.1);
            border-radius: 10px;
            text-shadow: 0 0 15px rgba(168, 184, 255, 0.4);
        }}

        ul {{
            list-style: none;
            margin: 20px 0;
        }}

        ul li {{
            margin: 10px 0;
            font-weight: bold;
            color: #ffd966;
            text-shadow: 0 0 10px rgba(255, 217, 102, 0.3);
        }}

        .cta {{
            background: rgba(30, 30, 70, 0.5);
            border: 1px solid rgba(168, 184, 255, 0.2);
            border-radius: 15px;
            padding: 40px 25px;
            margin: 40px 0;
            text-align: center;
            box-shadow: 0 4px 20px rgba(100, 100, 200, 0.2);
        }}

        .cta h2 {{
            border: none;
            margin: 20px 0;
        }}

        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, #4a5a9a, #6a7aca);
            color: white;
            text-decoration: none;
            padding: 20px 50px;
            border-radius: 35px;
            margin: 20px 0;
            font-size: 1.3em;
            font-weight: bold;
            box-shadow: 0 6px 25px rgba(74, 90, 154, 0.7);
            transition: all 0.3s ease;
            border: 2px solid rgba(168, 184, 255, 0.5);
        }}

        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(106, 122, 202, 0.9);
            background: linear-gradient(135deg, #5a6aaa, #7a8aca);
        }}

        .price {{
            font-size: 1.8em;
            color: #e8e8f0;
            margin: 20px 0 5px 0;
        }}

        .original-price {{
            text-decoration: line-through;
            color: #999;
            font-size: 1em;
        }}

        .special-price {{
            font-size: 2em;
            color: #ffd700;
            font-weight: bold;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
            white-space: nowrap;
        }}

        .limited-badge {{
            color: #ff4444;
            font-weight: bold;
            font-size: 0.95em;
            margin: 10px 0;
        }}

        .closing {{
            text-align: center;
            margin: 40px 0;
            padding: 30px 15px;
            background: rgba(60, 60, 120, 0.2);
            border-radius: 15px;
            font-size: 1.1em;
            line-height: 2;
        }}

        .signature {{
            text-align: right;
            font-size: 1.3em;
            color: #c8d0ff;
            margin-top: 30px;
        }}

        @media (max-width: 768px) {{
            body {{
                font-size: 15px;
                padding: 10px;
            }}

            .container {{
                padding: 20px 10px;
            }}

            h1 {{
                font-size: 1.3em;
            }}

            h2 {{
                font-size: 1.1em;
            }}

            .emoji-header {{
                font-size: 1.3em;
            }}

            .oracle-message,
            .section {{
                padding: 15px 10px;
            }}

            .oracle-message p {{
                font-size: 1em;
            }}

            .guardian {{
                font-size: 1.1em;
                padding: 15px;
            }}

            .price {{
                font-size: 1.5em;
            }}

            .special-price {{
                font-size: 1.8em;
            }}

            .cta-button {{
                font-size: 1.1em;
                padding: 15px 30px;
            }}

            .guardian-image {{
                max-width: 100%;
            }}

            .cta {{
                padding: 40px 15px;
            }}

            .closing {{
                padding: 30px 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{name}様　守護神鑑定書</h1>

        <div class="oracle-message">
            <p style="margin-bottom: 30px;">{name}様、</p>
            <p style="margin-bottom: 30px;">視えました。</p>
            <p class="guardian" style="margin-bottom: 30px;">あなたを守っているのは、<br>{guardian['full']}。</p>
            <p>{guardian['description']}</p>
            <img src="{guardian_image}" alt="{guardian['name']}" class="guardian-image">
        </div>

        <div class="section">
            {generate_intro_section(sections)}
        </div>

        <h2 class="emoji-header">⛩️お悩みについて</h2>
        <div class="section">
            {generate_troubles_section(sections['troubles'])}
        </div>

        <h2 class="emoji-header">⛩️なぜ今、<br>　悪いものを引き寄せているのか</h2>
        <div class="section">
            {generate_why_bad_section(sections['why_bad'])}
        </div>

        <h2 class="emoji-header">⛩️二つの道</h2>
        <div class="section">
            {generate_two_paths_section(sections['two_paths'])}
        </div>

        <h2 class="emoji-header">⛩️守護の方法</h2>
        <div class="section">
            {generate_method_section(sections['method'])}
        </div>

        {generate_four_items_section(sections['four_items'])}

        <div class="cta">
            <h2>【運命が動く24時間】</h2>
            {generate_cta_section(sections['cta'])}
        </div>

        <div class="closing">
            {generate_closing_section(sections['closing'])}
        </div>
    </div>
</body>
</html>
'''

    # 出力先を決定
    if output_dir is None:
        # txtファイルと同じディレクトリに作成
        base_dir = Path(txt_path).parent
        output_dir = base_dir / f"{name}様M"
    else:
        # 指定されたディレクトリ配下に作成
        output_dir = Path(output_dir) / f"{name}様M"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"

    # HTMLを保存
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ 完成: {output_path}")
    return output_path


def generate_intro_section(sections):
    """イントロセクションを生成（オーラ、守護神タイプ、本質）"""
    html_parts = []

    # オーラ
    if sections['aura']:
        content = sections['aura'].replace('\n', '<br>')
        html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    # 守護神タイプ
    if sections['guardian_type']:
        content = sections['guardian_type'].replace('\n', '<br>')
        html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    # 本質（黄色強調）
    if sections['essence']:
        content = sections['essence'].replace('\n', '<br>')
        html_parts.append(f'<p style="margin-bottom: 30px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">{content}</p>')

    # 流れが悪い
    if sections['flow_bad']:
        content = sections['flow_bad'].replace('\n', '<br>')
        html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    html_parts.append('<p>その原因をお伝えします。</p>')

    return '\n            '.join(html_parts)


def generate_troubles_section(text):
    """お悩みセクションを生成（最後の段落は白強調）"""
    paragraphs = text.split('\n\n')
    html_parts = []

    for i, para in enumerate(paragraphs):
        if not para.strip():
            continue
        content = para.replace('\n', '<br>')

        # 最後の段落かどうか、または「オーラを整え」で始まるか
        if i == len(paragraphs) - 1 or 'オーラを整え' in para:
            html_parts.append(f'<p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">{content}</p>')
        else:
            html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    return '\n            '.join(html_parts)


def generate_why_bad_section(text):
    """なぜ今セクションを生成（リスト項目を処理）"""
    # リスト項目を抽出
    list_items = extract_list_items(text)

    # リスト以外の部分
    text_without_list = re.sub(r'・[^\n]+\n?', '', text)
    paragraphs = [p.strip() for p in text_without_list.split('\n\n') if p.strip()]

    html_parts = []

    # 最初の段落（リストの前）
    if paragraphs:
        content = paragraphs[0].replace('\n', '<br>')
        html_parts.append(f'<p style="margin-bottom: 20px;">{content}</p>')

    # リスト
    if list_items:
        html_parts.append('<ul style="margin-bottom: 30px;">')
        for item in list_items:
            item_html = item.replace('\n', '<br>')
            html_parts.append(f'    <li>{item_html}</li>')
        html_parts.append('</ul>')

    # 残りの段落
    for para in paragraphs[1:]:
        content = para.replace('\n', '<br>')
        html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    return '\n            '.join(html_parts)


def generate_two_paths_section(text):
    """二つの道セクションを生成（特定の段落を白強調）"""
    paragraphs = text.split('\n\n')
    html_parts = []

    for para in paragraphs:
        if not para.strip():
            continue
        content = para.replace('\n', '<br>')

        # 「でも、ここで流れを変えたら」または「オーラが整い」で始まる段落は白強調
        if 'でも、ここで流れを変えたら' in para or 'オーラが整い' in para:
            html_parts.append(f'<p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">{content}</p>')
        else:
            html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    return '\n            '.join(html_parts)


def generate_method_section(text):
    """守護の方法セクションを生成"""
    paragraphs = text.split('\n\n')
    html_parts = []

    for para in paragraphs:
        if not para.strip():
            continue
        content = para.replace('\n', '<br>')

        # 「じゃあ、具体的に」で始まる段落は白強調
        if 'じゃあ、具体的に' in para or '理想の未来' in para:
            html_parts.append(f'<p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">{content}</p>')
        # 【本式守護鑑定】を含む段落
        elif '【本式守護鑑定】' in para or '【本格守護鑑定】' in para:
            # 【本式守護鑑定】を強調
            content = re.sub(r'【本[式格]守護鑑定】', r'<span style="font-size: 1.4em; font-weight: bold; color: #c8d0ff;">【本式守護鑑定】</span>', content)
            html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')
        else:
            html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    return '\n            '.join(html_parts)


def generate_four_items_section(items):
    """4つの項目セクションを生成"""
    if len(items) != 4:
        print(f"⚠️ 警告: 4項目ではなく{len(items)}項目が見つかりました")

    colors = [
        'rgba(255, 215, 0, 0.7)',    # 黄
        'rgba(255, 69, 58, 0.7)',    # 赤
        'rgba(52, 199, 89, 0.7)',    # 緑
        'rgba(0, 122, 255, 0.7)'     # 青
    ]

    html = '''<div style="padding: 40px 0; margin: 40px 0;">
            <h2 style="text-align: center; color: #c8d0ff; font-size: 1.3em; margin-bottom: 50px; border: none; text-shadow: 0 0 20px rgba(168, 184, 255, 0.5);">🔮 本式守護鑑定でお伝えすること</h2>

            <div style="margin: 30px 0; text-align: center;">'''

    for i, item in enumerate(items[:4]):
        color = colors[i] if i < len(colors) else colors[0]

        # タイトルと説明を分離
        lines = item.split('\n', 1)
        title = lines[0].strip()
        description = lines[1].strip() if len(lines) > 1 else ''

        # 改行を<br>に変換
        title_html = title.replace('\n', '<br>')
        desc_html = description.replace('\n', '<br>')

        html += f'''
                <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: {color}; opacity: 0.3;"></div>
                    <div style="position: relative; z-index: 1;">
                        <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ {title_html}</h3>
                        <p>{desc_html}</p>
                    </div>
                </div>'''

    html += '''
            </div>

            <p style="margin-top: 30px; text-align: center;">このまま方法を知らずに過ごすか、<br>守護を受け取る道を選ぶか。<br>決めるのは、あなたです。</p>
        </div>'''

    return html


def generate_cta_section(text):
    """CTAセクションを生成"""
    paragraphs = text.split('\n\n')
    html_parts = []

    for para in paragraphs:
        if not para.strip():
            continue
        content = para.replace('\n', '<br>')

        # 守護霊の声（「この人は」で始まる段落）
        if '「この人は' in para or '力を貸してあげたい' in para or '運命を動かす手助け' in para:
            html_parts.append(f'<p style="margin-bottom: 30px; font-size: 1.15em; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">{content}</p>')
        # 「ただ、今から24時間」
        elif 'ただ、今から24時間' in para:
            html_parts.append(f'<p style="margin-bottom: 30px; font-weight: bold;">{content}</p>')
        # 価格情報
        elif '通常9,800円' in para or '9800円' in para:
            html_parts.append('''<div class="price">
                <span class="original-price">通常9,800円</span><br>
                <span class="limited-badge">24時間限定の特別価格</span><br>
                <span class="special-price">4,980円</span>
            </div>''')
        # リンク
        elif 'https://' in para:
            html_parts.append('<a href="https://lnuwhrs3tncycy5pf0r3.stores.jp/items/69eb763d23b5d0e88f9854e9" class="cta-button" target="_blank">本式守護鑑定を受ける▼</a>')
        # その他の段落
        else:
            # 価格行と▼行はスキップ
            if '4,980円' in para or '4980円' in para or '▼' in para:
                continue
            html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    return '\n            '.join(html_parts)


def generate_closing_section(text):
    """クロージングセクションを生成"""
    paragraphs = text.split('\n\n')
    html_parts = []

    for para in paragraphs:
        if not para.strip():
            continue

        # 署名は別処理
        if '深幸' in para or '深雪' in para:
            html_parts.append('<div class="signature">深雪</div>')
            continue

        content = para.replace('\n', '<br>')

        # ビジョン部分（長めの段落）を太字に
        if len(para) > 50 and ('が。' in para or '場面が。' in para or '未来が。' in para):
            html_parts.append(f'<p style="margin-bottom: 30px; font-weight: bold;">{content}</p>')
        elif 'その未来へ' in para:
            html_parts.append(f'<p style="margin-bottom: 40px;">{content}</p>')
        else:
            html_parts.append(f'<p style="margin-bottom: 30px;">{content}</p>')

    return '\n            '.join(html_parts)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使い方: python txt_to_html.py <txtファイルパス> [出力ディレクトリ]")
        print("例: python txt_to_html.py 無料鑑定/深雪/001_みわ_復縁相談_深幸.txt")
        sys.exit(1)

    txt_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    generate_html(txt_path, output_dir)
