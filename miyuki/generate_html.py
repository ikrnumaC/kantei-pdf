#!/usr/bin/env python3
"""深雪さん用 鑑定HTMLジェネレータ - txt→HTML変換"""
import re
import sys
from pathlib import Path

# 守護神名 → (aura_color_1, aura_color_2)
AURA_COLORS = {
    "火産霊神": ("255, 180, 100", "255, 120, 60"),
    "奥津日子命": ("255, 180, 100", "255, 120, 60"),
    "迦楼羅天": ("255, 180, 100", "255, 120, 60"),
    "火之迦具土神": ("255, 140, 90", "230, 80, 50"),
    "三宝荒神": ("255, 140, 90", "230, 80, 50"),
    "不動明王": ("255, 120, 80", "210, 60, 40"),
    "豊玉姫": ("120, 200, 255", "60, 140, 220"),
    "市杵嶋姫命": ("120, 200, 255", "60, 140, 220"),
    "住吉大神": ("120, 200, 255", "60, 140, 220"),
    "綿津見神": ("90, 160, 220", "40, 100, 180"),
    "弁財天": ("170, 200, 255", "110, 150, 220"),
    "瀬織津姫": ("180, 220, 255", "100, 170, 230"),
    "罔象女神": ("180, 220, 255", "100, 170, 230"),
    "弥都波能売神": ("180, 220, 255", "100, 170, 230"),
    "速秋津日子・比売神": ("180, 220, 255", "100, 170, 230"),
    "闇淤加美神": ("110, 150, 210", "60, 100, 170"),
    "高淤加美神": ("110, 150, 210", "60, 100, 170"),
    "龍樹菩薩": ("160, 180, 240", "110, 130, 210"),
    "久久能智神": ("180, 230, 150", "120, 180, 90"),
    "五十猛命": ("180, 230, 150", "120, 180, 90"),
    "木俣神": ("180, 230, 150", "120, 180, 90"),
    "鹿屋野比売": ("200, 230, 160", "140, 190, 100"),
    "大山祇神": ("150, 200, 140", "90, 150, 80"),
    "白山比咩神": ("230, 240, 230", "180, 210, 180"),
    "木花咲耶姫": ("255, 180, 210", "230, 130, 180"),
    "吉祥天": ("255, 200, 220", "230, 150, 200"),
    "埴山姫神": ("220, 180, 140", "180, 130, 80"),
    "埴山彦神": ("220, 180, 140", "180, 130, 80"),
    "大地主神": ("220, 180, 140", "180, 130, 80"),
    "春日大明神": ("230, 200, 150", "190, 150, 90"),
    "金山姫神": ("240, 220, 160", "200, 170, 100"),
    "金山彦神": ("240, 220, 160", "200, 170, 100"),
    "毘沙門天": ("230, 210, 140", "180, 160, 80"),
    "布都御魂": ("220, 230, 240", "170, 180, 200"),
    "経津主神": ("220, 230, 240", "170, 180, 200"),
    "日本武尊": ("210, 225, 240", "160, 180, 210"),
    "建御雷神": ("200, 170, 255", "150, 100, 220"),
    "天照大御神": ("255, 230, 130", "255, 180, 80"),
    "宇迦之御魂神": ("255, 220, 140", "230, 170, 80"),
    "豊受大神": ("255, 225, 150", "230, 180, 90"),
    "吒枳尼天": ("255, 200, 120", "230, 160, 70"),
    "大己貴命": ("180, 210, 130", "130, 170, 80"),
    "猿田彦命": ("255, 200, 100", "230, 150, 50"),
    "天之御中主神": ("230, 220, 255", "190, 180, 230"),
    "高御産巣日神": ("240, 230, 255", "200, 190, 235"),
}

# 日柱天干(十干) → 元素背景画像
ELEMENT_IMAGES = {
    "甲": "深い森.jpg",
    "乙": "若葉.jpg",
    "丙": "太陽.gif",
    "丁": "ろうそく.jpg",
    "戊": "大地.jpg",
    "己": "肥沃な大地.webp",
    "庚": "刀.png",
    "辛": "宝石.jpg",
    "壬": "深海.jpg",
    "癸": "水面.jpg",
}

# 壬水(深海.jpg)は元画像が暗いのでフィルターを上書き
ELEMENT_FILTER_OVERRIDES = {
    "壬": ("blur(1.5px) brightness(1.5) contrast(1.2)", "0.6"),
}
DEFAULT_ELEMENT_FILTER = ("blur(1.5px) brightness(0.85)", "0.4")

# 黄色ハイライトするマーカー(fragment match)
YELLOW_MARKERS = [
    "自分の状態を正しく知るか",
    "ご自分の流れを",
    "この巡り合わせは",
    "止まっていた運命",
]

def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def paragraph_html(text, yellow=False, cls=None, mb=90):
    text = text.strip("\n")
    # convert internal newlines to <br>
    lines = [html_escape(l) for l in text.split("\n") if l != ""]
    inner = "<br>".join(lines)
    styles = [f"margin-bottom: {mb}px"]
    if yellow:
        styles.append("color: #ffd966")
        styles.append("font-weight: bold")
        styles.append("text-shadow: 0 0 15px rgba(255, 217, 102, 0.4)")
    style = "; ".join(styles) + ";"
    cls_attr = f' class="{cls}"' if cls else ""
    return f'            <p{cls_attr} style="{style}">{inner}</p>'

def is_yellow_para(text):
    t = text.replace("\n", "")
    for m in YELLOW_MARKERS:
        if m in t:
            return True
    return False

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Google tag (gtag.js) : GA4 計測 [GA4-MIYUKI] -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JHLDFT6DR7"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-JHLDFT6DR7');
    </script>
    <title>{name}様　守護神鑑定書</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'YuMincho', serif; background: linear-gradient(135deg, #1a1a3e 0%, #0f0f2e 50%, #1a1a3e 100%); color: #e8e8f0; line-height: 1.8; padding: 20px; min-height: 100vh; font-size: 17px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: none; border-radius: 20px; padding: 40px; box-shadow: none; border: none; }}
        h1 {{ text-align: center; color: #a8b8ff; font-size: 2em; margin-bottom: 30px; text-shadow: 0 0 20px rgba(168, 184, 255, 0.5); letter-spacing: 0.1em; }}
        h2 {{ color: #c8d0ff; font-size: 1.5em; margin: 40px 0 20px; padding-bottom: 10px; border-bottom: 2px solid rgba(168, 184, 255, 0.3); letter-spacing: 0.05em; }}
        .oracle-message {{ background: linear-gradient(135deg, rgba(60, 60, 120, 0.3), rgba(40, 40, 100, 0.3)); border: 2px solid rgba(168, 184, 255, 0.3); border-radius: 15px; padding: 30px; margin: 30px 0; box-shadow: 0 4px 20px rgba(100, 100, 200, 0.2); position: relative; }}
        .oracle-message::before {{ content: ''; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); font-size: 30px; background: #1a1a3e; padding: 0 15px; }}
        .guardian-image {{ max-width: 400px; width: 100%; height: auto; margin: 30px auto; display: block; border-radius: 10px; box-shadow: 0 4px 20px rgba(168, 184, 255, 0.3); }}
        .oracle-message p {{ margin: 15px 0; text-align: center; font-size: 1.1em; }}
        .section {{ margin: 30px 0; padding: 20px; background: rgba(30, 30, 70, 0.3); border-radius: 10px; text-align: center; }}
        .emoji-header {{ font-size: 1.8em; margin: 40px 0 20px; color: #c8d0ff; text-align: left; }}
        .guardian {{ text-align: center; font-size: 1.3em; color: #a8b8ff; margin: 20px 0; padding: 20px; background: rgba(168, 184, 255, 0.1); border-radius: 10px; text-shadow: 0 0 15px rgba(168, 184, 255, 0.4); }}
        ul {{ list-style: none; margin: 20px 0; }}
        ul li {{ margin: 10px 0; font-weight: bold; color: #ffd966; text-shadow: 0 0 10px rgba(255, 217, 102, 0.3); }}
        .cta {{ background: rgba(30, 30, 70, 0.5); border: 1px solid rgba(168, 184, 255, 0.2); border-radius: 15px; padding: 40px 25px; margin: 40px 0; text-align: center; box-shadow: 0 4px 20px rgba(100, 100, 200, 0.2); }}
        .cta h2 {{ border: none; margin: 20px 0; }}
        .cta-button {{ display: inline-block; background: linear-gradient(135deg, #4a5a9a, #6a7aca); color: white; text-decoration: none; padding: 20px 50px; border-radius: 35px; margin: 20px 0; font-size: 1.3em; font-weight: bold; box-shadow: 0 6px 25px rgba(74, 90, 154, 0.7); transition: all 0.3s ease; border: 2px solid rgba(168, 184, 255, 0.5); }}
        .cta-button:hover {{ transform: translateY(-3px); box-shadow: 0 8px 30px rgba(106, 122, 202, 0.9); background: linear-gradient(135deg, #5a6aaa, #7a8aca); }}
        .price {{ font-size: 1.8em; color: #e8e8f0; margin: 20px 0 5px 0; }}
        .original-price {{ text-decoration: line-through; color: #999; font-size: 1em; }}
        .special-price {{ font-size: 2em; color: #ffd700; font-weight: bold; text-shadow: 0 0 20px rgba(255, 215, 0, 0.6); white-space: nowrap; }}
        .limited-badge {{ color: #ff4444; font-weight: bold; font-size: 0.95em; margin: 10px 0; }}
        .closing {{ text-align: center; margin: 40px 0; padding: 30px 15px; background: rgba(60, 60, 120, 0.2); border-radius: 15px; font-size: 1.1em; line-height: 2; }}
        .signature {{ text-align: right; font-size: 1.3em; color: #c8d0ff; margin-top: 30px; }}
        :root {{ --aura-color-1: {aura1}; --aura-color-2: {aura2}; }}
        .reveal {{ opacity: 0; transform: translateY(30px); transition: opacity 1.2s ease-out, transform 1.2s ease-out; }}
        .reveal.is-visible {{ opacity: 1; transform: translateY(0); }}
        .guardian-image {{ position: relative; animation: aura-breath 4s ease-in-out infinite; }}
        @keyframes aura-breath {{
            0%, 100% {{ box-shadow: 0 0 30px rgba(var(--aura-color-1), 0.35), 0 0 60px rgba(var(--aura-color-2), 0.2), 0 4px 20px rgba(168, 184, 255, 0.3); }}
            50% {{ box-shadow: 0 0 50px rgba(var(--aura-color-1), 0.6), 0 0 100px rgba(var(--aura-color-2), 0.35), 0 4px 20px rgba(168, 184, 255, 0.3); }}
        }}
        .cta-button {{ animation: pulse 2.4s ease-in-out infinite; }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 6px 25px rgba(74, 90, 154, 0.7); }}
            50% {{ transform: scale(1.035); box-shadow: 0 8px 35px rgba(168, 184, 255, 0.9), 0 0 40px rgba(168, 184, 255, 0.4); }}
        }}
        .cta-button:hover {{ animation: none; }}

        /* ===== 演出：元素の背景（冒頭〜神様登場まで） ===== */
        .element-bg {{
            position: fixed;
            inset: 0;
            z-index: -4;
            background-image: url("../鑑定画像/{element_image}");
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center;
            filter: {element_filter};
            opacity: {element_opacity};
            pointer-events: none;
            transition: opacity 1.4s ease;
        }}
        .element-bg.is-hidden {{ opacity: 0; }}

        /* ===== 演出：神様の背景（神様登場〜本式4メニューの手前まで） ===== */
        .deity-bg {{
            position: fixed;
            inset: 0;
            z-index: -3;
            background-image: url("../鑑定画像/{guardian}.png");
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center 18%;
            filter: blur(1.5px) brightness(0.85);
            opacity: 0;
            pointer-events: none;
            transition: opacity 1.4s ease;
        }}
        .deity-bg.is-visible {{ opacity: 0.4; }}

        /* ===== 演出：本式4メニュー〜クロージングは扉の背景に続ける ===== */
        .door-bg {{
            position: fixed;
            inset: 0;
            z-index: -3;
            background-image: url("../鑑定画像/ドア2.jpg");
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center;
            filter: blur(1.5px) brightness(0.85);
            opacity: 0;
            pointer-events: none;
            transition: opacity 1.4s ease;
        }}
        .door-bg.is-visible {{ opacity: 0.4; }}

        .deity-veil {{
            position: fixed;
            inset: 0;
            z-index: -2;
            pointer-events: none;
            background:
                radial-gradient(ellipse at 50% 20%, rgba(15, 15, 46, 0.15) 0%, rgba(15, 15, 46, 0.55) 60%, rgba(15, 15, 46, 0.85) 100%),
                linear-gradient(180deg, rgba(15, 15, 46, 0.25) 0%, rgba(15, 15, 46, 0.7) 100%);
        }}
        @media (max-width: 768px) {{
            body {{ font-size: 15px; padding: 10px; }}
            .container {{ padding: 20px 10px; }}
            h1 {{ font-size: 1.3em; }}
            h2 {{ font-size: 1.1em; }}
            .emoji-header {{ font-size: 1.3em; }}
            .oracle-message, .section {{ padding: 15px 10px; }}
            .oracle-message p {{ font-size: 1em; }}
            .guardian {{ font-size: 1.1em; padding: 15px; }}
            .price {{ font-size: 1.5em; }}
            .special-price {{ font-size: 1.8em; }}
            .cta-button {{ font-size: 1.1em; padding: 15px 30px; }}
            .cta {{ padding: 40px 15px; }}
            .closing {{ padding: 30px 10px; }}
            .guardian-image {{ max-width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="element-bg" id="elementBg"></div>
    <div class="deity-bg" id="deityBg"></div>
    <div class="door-bg" id="doorBg"></div>
    <div class="deity-veil"></div>
    <div class="container">
        <h1>{name}様<br>守護神鑑定書</h1>

{body}
    </div>
    <script>
    /* ===== 演出：背景の切り替え（元素 → 神様登場で神様に → 4メニュー手前で扉に） ===== */
    (function () {{
        var elementBg = document.getElementById('elementBg');
        var deityBg = document.getElementById('deityBg');
        var doorBg = document.getElementById('doorBg');
        var guardianSentinel = document.getElementById('guardianSentinel');
        var deitySentinel = document.getElementById('deitySentinel');
        if (!elementBg || !deityBg || !doorBg || !guardianSentinel || !deitySentinel) return;

        var layers = [elementBg, deityBg, doorBg];
        function show(active) {{
            layers.forEach(function (el) {{
                if (el === active) el.classList.add('is-visible');
                else el.classList.remove('is-visible');
            }});
            elementBg.classList.toggle('is-hidden', active !== elementBg);
        }}

        function onScroll() {{
            var trigger = window.innerHeight * 0.65;
            var guardianReached = guardianSentinel.getBoundingClientRect().top < trigger;
            var doorReached = deitySentinel.getBoundingClientRect().top < trigger;

            if (!guardianReached) {{
                show(elementBg);
            }} else if (!doorReached) {{
                show(deityBg);
            }} else {{
                show(doorBg);
            }}
        }}
        window.addEventListener('scroll', onScroll, {{ passive: true }});
        onScroll();
    }})();
    </script>
    <script>
        (function () {{
            var els = document.querySelectorAll('.reveal');
            if (!('IntersectionObserver' in window)) {{
                els.forEach(function (el) {{ el.classList.add('is-visible'); }});
                return;
            }}
            var io = new IntersectionObserver(function (entries) {{
                entries.forEach(function (e) {{
                    if (e.isIntersecting) {{
                        e.target.classList.add('is-visible');
                        io.unobserve(e.target);
                    }}
                }});
            }}, {{ threshold: 0.12, rootMargin: '0px 0px -40px 0px' }});
            els.forEach(function (el) {{ io.observe(el); }});
        }})();
    </script>
<!-- GA4 カスタム計測：誰が/最後まで読んだか/購入ボタン [GA4-MIYUKI] -->
<script>
(function () {{
  function fire() {{
    var seg = location.pathname.split('/').filter(Boolean);
    var last = decodeURIComponent(seg[seg.length - 1] || '');
    var id = /\\.html?$/i.test(last) ? decodeURIComponent(seg[seg.length - 2] || 'unknown') : (last || 'unknown');
    var base = {{ kantei_id: id, persona: 'miyuki' }};
    gtag('set', 'user_properties', {{ kantei_id: id, persona: 'miyuki' }});
    gtag('event', 'page_open', base);

    var end = document.querySelector('.signature, .sign');
    if (end && 'IntersectionObserver' in window) {{
      var done = false;
      var io = new IntersectionObserver(function (es) {{
        es.forEach(function (e) {{
          if (e.isIntersecting && !done) {{ done = true; gtag('event', 'read_complete', base); io.disconnect(); }}
        }});
      }}, {{ threshold: 0.5 }});
      io.observe(end);
    }}

    document.querySelectorAll('.cta-button, .btn').forEach(function (b) {{
      b.addEventListener('click', function () {{ gtag('event', 'cta_click', base); }});
    }});
  }}
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fire); else fire();
}})();
</script>

</body>
</html>
"""

BOX_COLORS = [
    "rgba(255, 215, 0, 0.7)",   # yellow
    "rgba(255, 69, 58, 0.7)",   # red
    "rgba(52, 199, 89, 0.7)",   # green
    "rgba(0, 122, 255, 0.7)",   # blue
]


def parse_txt(path):
    """Parse txt file and return structured data."""
    text = Path(path).read_text(encoding="utf-8")
    lines = text.split("\n")

    # 命式ヘッダー
    name = None
    guardian_name = None
    guardian_reading = None
    aura_line = None
    day_stem = None
    for i, ln in enumerate(lines):
        if ln.startswith("【") and "様の命式" in ln and name is None:
            m = re.match(r"【(.+?)様の命式】", ln)
            if m:
                name = m.group(1)
        if ln.startswith("日柱:") and day_stem is None:
            m = re.search(r"日柱[:：]\s*([甲乙丙丁戊己庚辛壬癸])", ln)
            if m:
                day_stem = m.group(1)
        if ln.startswith("オーラ:") and aura_line is None:
            aura_line = ln.split(":", 1)[1].strip()
        if ln.startswith("守護神:") and guardian_name is None:
            g = ln.split(":", 1)[1].strip()
            m = re.match(r"([^\(（]+)[\(（](.+?)[\)）]", g)
            if m:
                guardian_name = m.group(1).strip()
                guardian_reading = m.group(2).strip()
            else:
                guardian_name = g

    # find separator
    sep_i = None
    for i, ln in enumerate(lines):
        if "━" in ln and ln.count("━") > 5:
            sep_i = i
            break
    if sep_i is None:
        raise ValueError("separator not found in " + path)

    body = "\n".join(lines[sep_i + 1:])

    # Fallback: extract guardian from body if not in header
    if not guardian_name:
        # look for "あなたを守っているのは\n<NAME>（<reading>）" (parens may be on next line)
        m = re.search(r"あなたを守っているのは\s*\n\s*([^\n（(]+?)\s*\n?\s*[（(]([^）)]+)[）)]", body)
        if m:
            guardian_name = m.group(1).strip()
            guardian_reading = m.group(2).strip()

    return {
        "name": name,
        "guardian": guardian_name,
        "reading": guardian_reading,
        "aura": aura_line,
        "day_stem": day_stem,
        "body": body,
    }


def split_paragraphs(text):
    """Split text by blank lines into paragraphs. Each paragraph keeps internal newlines."""
    text = text.strip("\n")
    paras = re.split(r"\n\s*\n", text)
    return [p.strip("\n") for p in paras if p.strip()]


HEADER_BR = "\x01BR\x01"


def merge_multiline_headers(body):
    """Some ⛩️ headers wrap onto a second line with no blank line in between
    (blank line comes after the full header, before the section body). Merge
    those two lines into one so the header-split regex treats them as a unit."""
    lines = body.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("⛩️") and i + 1 < len(lines):
            nxt = lines[i + 1]
            after = lines[i + 2] if i + 2 < len(lines) else ""
            if nxt.strip() != "" and not nxt.startswith("⛩️") and after.strip() == "":
                line = line + HEADER_BR + nxt.strip()
                i += 1
        out.append(line)
        i += 1
    return "\n".join(out)


def build_body_html(data):
    name = data["name"]
    guardian = data["guardian"]
    reading = data["reading"]
    body = data["body"].replace(
        "【本式守護鑑定でお伝えすること】", "⛩️本式守護鑑定でお伝えすること"
    )
    body = merge_multiline_headers(body)

    # Split into major sections by ⛩️ headers
    # First section: everything before first ⛩️
    parts = re.split(r"(⛩️[^\n]+)", body)
    # parts alternates: [pre_intro, header1, content1, header2, content2, ...]

    pre_intro = parts[0]  # includes intro + guardian intro + first content up to ⛩
    sections = []
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        content = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((header, content))

    html_parts = []

    # === Oracle-message + first .section (intro + character analysis) ===
    intro_paras = split_paragraphs(pre_intro)

    # First 4 paragraphs → oracle-message (name, 霊視して驚きました, aura desc, 守護神からの守護も)
    # find where "本来" or similar starts the body section
    # We split at the paragraph that includes the guardian intro (あなたを守っているのは)
    guardian_intro_idx = None
    for i, p in enumerate(intro_paras):
        if "あなたを守っているのは" in p or "守っているのは" in p:
            guardian_intro_idx = i
            break

    # Oracle message: first 4 paragraphs
    oracle_paras = intro_paras[:4]
    body_paras = intro_paras[4:guardian_intro_idx] if guardian_intro_idx else intro_paras[4:]
    guardian_paras = intro_paras[guardian_intro_idx:] if guardian_intro_idx else []

    # --- oracle message block ---
    html_parts.append('        <div class="oracle-message reveal">')
    for i, p in enumerate(oracle_paras):
        # aura line (3rd paragraph typically) → yellow
        yellow = i == 2  # "これほど〜纏った...なかなかいらっしゃいません" is aura
        html_parts.append(paragraph_html(p, yellow=yellow))
    html_parts.append('        </div>')
    html_parts.append('')

    # --- body section with character analysis + guardian ---
    html_parts.append('        <div class="section reveal">')
    for i, p in enumerate(body_paras):
        yellow = is_yellow_para(p)
        # First paragraph = character intro → yellow
        if i == 0 and p.startswith(name + "様"):
            yellow = True
        # "だから今" ぶつかりの説明 → yellow
        if "だから今" in p and ("ぶつかって" in p or "揺れていて" in p):
            yellow = True
        if p.strip() == "でも、大丈夫です。":
            yellow = True
        if "その答えの出し方" in p or "その整え方" in p:
            yellow = True
        html_parts.append(paragraph_html(p, yellow=yellow))

    # Guardian paragraphs
    if guardian_paras:
        # First one: "あなたを守っているのは\nX(reading)。"
        first_g = guardian_paras[0]
        consumed = 1
        # Some texts split the guardian name into its own paragraph block
        # (e.g. "のりちゃん様を\n守っているのは" / "住吉大神(すみよしのおおかみ)。")
        # — merge them so the name still renders in the glowing guardian box.
        name_in_first = bool(guardian) and guardian in first_g
        if not name_in_first and len(guardian_paras) > 1 and guardian and guardian in guardian_paras[1]:
            first_g = first_g + "\n" + guardian_paras[1]
            consumed = 2
        html_parts.append('            <div id="guardianSentinel"></div>')
        html_parts.append(paragraph_html(first_g, cls="guardian"))
        # second: guardian short description (before image)
        if len(guardian_paras) > consumed:
            desc = guardian_paras[consumed]
            # No margin (image comes next)
            text = desc.strip("\n")
            lines_ = [html_escape(l) for l in text.split("\n") if l]
            inner = "<br>".join(lines_)
            html_parts.append(f'            <p>{inner}</p>')
        # image
        html_parts.append(f'            <img src="../鑑定画像/{guardian}.png" alt="{guardian}" class="guardian-image">')
        # remaining guardian paragraphs
        for p in guardian_paras[consumed + 1:]:
            html_parts.append(paragraph_html(p, yellow=False))

    html_parts.append('        </div>')
    html_parts.append('')

    # === ⛩️ sections ===
    for idx, (header, content) in enumerate(sections):
        header_text = header.replace("⛩️", "").strip()

        # Special: 本式守護鑑定でお伝えすること — has 🌙 items
        has_moon_items = "🌙" in content

        # Split header on 様 to add br after 様 for long headers
        # e.g. "タダオ様のご縁が動く流れ" → "タダオ様<br>ご縁が動く流れ"
        # But only if header is long. Simple: don't force br.
        # Actually template uses br sometimes but not always. Keep simple.
        h_html = html_escape(header_text).replace(HEADER_BR, "<br>")

        html_parts.append(f'        <h2 class="emoji-header">⛩️{h_html}</h2>')

        if has_moon_items:
            # Split content into pre-moon body + moon items
            # Moon items start with 🌙 and have a title + indented desc
            # Split at first 🌙
            moon_idx = content.find("🌙")
            pre = content[:moon_idx]
            moon_block = content[moon_idx:]
            # Cut moon_block at 【 (運命の扉) if present
            cta_idx = moon_block.find("【")
            if cta_idx != -1:
                moon_block = moon_block[:cta_idx]

            # Handle "本式守護鑑定で\nX様にお渡しするのは" - that's typically the last para of pre
            pre_paras = split_paragraphs(pre)

            # 特殊: 【運命の扉が開く24時間】 might appear later
            # If pre_paras contains anything after moon items (won't in this format)

            html_parts.append('        <div class="section reveal">')
            for p in pre_paras:
                yellow = is_yellow_para(p)
                html_parts.append(paragraph_html(p, yellow=yellow))
            html_parts.append('        </div>')
            html_parts.append('')

            # Parse moon items
            moon_pattern = re.compile(r"🌙\s*([^\n]+)\n((?:  [^\n]+\n?)+)")
            # Some are indented with two spaces; capture until next 🌙 or blank+non-indent
            # Simpler: split by 🌙
            items = re.split(r"🌙\s*", moon_block)
            items = [it.strip("\n") for it in items if it.strip()]

            # Each item: first line = title, rest = description (indented lines)
            parsed_items = []
            for it in items:
                lines_ = it.split("\n")
                title = lines_[0].strip()
                # description lines (indented or flat). Stop at the closing boilerplate
                # ("あなたご自身の手で...") which follows the last item with no further 🌙 to bound it.
                desc_lines = []
                for l in lines_[1:]:
                    s = l.strip().lstrip("　")
                    if s == "":
                        continue
                    if s.startswith("あなたご自身の手で"):
                        break
                    desc_lines.append(s)
                parsed_items.append((title, desc_lines))
                if len(parsed_items) == 4:
                    break

            # Trailing content after moon items (until 【)
            # Grab from moon_block: after last item block, before 【運命
            trailing = ""
            m_end = re.search(r"【運命の扉が開く24時間】", body)
            if m_end:
                trailing_start = body.find("🌙")
                # more robust: find text between last moon item's end and 【
                # Try: everything between last "🌙 ○○らしい〜方" block and 【
                # Assume the trailing sits between the item list and the CTA block.
                # Extract from moon_block:
                # find "【運命の扉が開く24時間】" in body → parts after are CTA
                pass

            # Boxes
            html_parts.append('        <div id="deitySentinel"></div>')
            html_parts.append('')
            html_parts.append('        <div style="padding: 40px 0; margin: 40px 0;">')
            html_parts.append('            <div style="margin: 30px 0; text-align: center;">')
            for k, (title, desc) in enumerate(parsed_items[:4]):
                bg = BOX_COLORS[k]
                title_html = html_escape(title)
                # Add <br> in title if long (contains 3+ char before の or 〜)
                # Simpler: use as-is
                desc_html = "<br>".join(html_escape(d) for d in desc)
                html_parts.append(f'                <div class="reveal" style="position: relative; padding: 40px 30px; margin-bottom: 0;">')
                html_parts.append(f'                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: {bg}; opacity: 0.3;"></div>')
                html_parts.append(f'                    <div style="position: relative; z-index: 1;">')
                html_parts.append(f'                        <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">🌙 {title_html}</h3>')
                html_parts.append(f'                        <p>{desc_html}</p>')
                html_parts.append(f'                    </div>')
                html_parts.append(f'                </div>')
                html_parts.append('')
            html_parts.append('            </div>')
            html_parts.append('')
            # Closing lines after items
            html_parts.append(f'            <p style="margin-top: 90px; margin-bottom: 90px; text-align: center;">{name}様ご自身の手で<br>未来を選び取るための鑑定です。</p>')
            html_parts.append(f'            <p style="margin-top: 90px; margin-bottom: 90px; text-align: center; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">その一歩を<br>ここから踏み出してください。</p>')
            html_parts.append('        </div>')
            html_parts.append('')

            # Now process trailing 【運命の扉が開く24時間】 CTA + closing
            m = re.search(r"【運命の扉が開く24時間】(.*?)▼ 本式守護霊視鑑定はこちら\s*\n(https?://\S+)(.*?)$", body, re.DOTALL)
            if m:
                cta_body = m.group(1).strip()
                url = m.group(2).strip()
                after = m.group(3).strip()

                # cta_body paragraphs
                cta_paras = split_paragraphs(cta_body)
                html_parts.append('        <div class="cta reveal">')
                html_parts.append('            <h2>【運命の扉が開く24時間】</h2>')
                html_parts.append('')
                # Custom formatting: normal + yellow highlights per markers
                # Also filter out the "通常20,000円のところ..." price line
                price_para_idx = None
                for i, p in enumerate(cta_paras):
                    if "通常20,000円" in p or "通常20000円" in p:
                        price_para_idx = i
                        break

                for i, p in enumerate(cta_paras):
                    yellow = is_yellow_para(p)
                    html_parts.append(paragraph_html(p, yellow=yellow))

                html_parts.append('')
                html_parts.append('            <div class="price">')
                html_parts.append('                <span class="original-price">通常9,800円</span><br>')
                html_parts.append('                <span class="limited-badge">24時間限定の特別価格</span><br>')
                html_parts.append('                <span class="special-price">4,980円</span>')
                html_parts.append('            </div>')
                html_parts.append('')
                html_parts.append(f'            <a href="{url}" class="cta-button" target="_blank">本式守護鑑定を受ける▼</a>')
                html_parts.append('')
                html_parts.append('            <p style="margin-top: 90px;">お申し込み後、<br>購入時のお名前をお知らせください。<br>1日以内に、<br>あなただけの鑑定書をお届けします。</p>')
                html_parts.append('        </div>')
                html_parts.append('')

                # closing
                after_paras = split_paragraphs(after)
                # Remove "深雪" line if it's a standalone
                after_paras = [p for p in after_paras if p.strip() not in ("深雪",)]

                html_parts.append('        <div class="closing reveal">')
                for i, p in enumerate(after_paras):
                    yellow = i == 0 or is_yellow_para(p)
                    # Only first paragraph yellow (物語がXらしい結末を迎えることを...)
                    if "物語が" in p and "結末" in p:
                        yellow = True
                    else:
                        yellow = False
                    html_parts.append(paragraph_html(p, yellow=yellow))
                html_parts.append('')
                html_parts.append('            <div class="signature">深雪</div>')
                html_parts.append('        </div>')

        else:
            # Regular section
            content_paras = split_paragraphs(content)
            html_parts.append('        <div class="section reveal">')
            for p in content_paras:
                yellow = is_yellow_para(p)
                html_parts.append(paragraph_html(p, yellow=yellow))
            html_parts.append('        </div>')
            html_parts.append('')

    return "\n".join(html_parts)


def generate(txt_path, out_dir):
    data = parse_txt(txt_path)
    aura1, aura2 = AURA_COLORS.get(data["guardian"], ("168, 184, 255", "100, 100, 200"))
    element_image = ELEMENT_IMAGES.get(data["day_stem"], "若葉.jpg")
    element_filter, element_opacity = ELEMENT_FILTER_OVERRIDES.get(data["day_stem"], DEFAULT_ELEMENT_FILTER)
    body = build_body_html(data)
    html = TEMPLATE.format(
        name=data["name"],
        aura1=aura1,
        aura2=aura2,
        guardian=data["guardian"],
        element_image=element_image,
        element_filter=element_filter,
        element_opacity=element_opacity,
        body=body,
    )

    out_path = Path(out_dir) / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) == 3:
        txt = sys.argv[1]
        out = sys.argv[2]
        p = generate(txt, out)
        print(f"Generated: {p}")
    else:
        SRC_DIR = Path("/Users/miura/Documents/GitHub/kantei/無料鑑定/深雪")
        OUT_DIR = Path("/Users/miura/Documents/GitHub/kantei/miyuki")
        TARGETS = [
            (996, "みむ", "996_みむ_お別れと次の恋相談_深雪.txt"),
            (997, "なおこ", "997_なおこ_子育てと守護霊相談_深雪.txt"),
            (998, "はるな", "998_はるな_復縁相談_深雪.txt"),
            (999, "かなめ", "999_かなめ_穏やかな関係相談_深雪.txt"),
            (1000, "レナ", "1000_レナ_借金完済と金運相談_深雪.txt"),
            (1001, "えなこ", "1001_えなこ_娘との関係相談_深雪.txt"),
            (1002, "みー", "1002_みー_社会復帰不安相談_深雪.txt"),
            (1003, "yossy", "1003_yossy_部活の保護者との関係_深雪.txt"),
            (1004, "ゆー", "1004_ゆー_進路と人間関係相談_深雪.txt"),
            (1005, "まり", "1005_まり_仕事の運相談_深雪.txt"),
            (1006, "ユキノ", "1006_ユキノ_闘病と再婚生活の願い_深雪.txt"),
            (1007, "よ", "1007_よ_復縁相談_深雪.txt"),
            (1008, "やす", "1008_やす_恋愛仕事プライベート相談_深雪.txt"),
            (1009, "のりこ", "1009_のりこ_娘との関係相談_深雪.txt"),
            (1010, "あゆか", "1010_あゆか_金運相談_深雪.txt"),
            (1011, "mimi", "1011_mimi_パニック障害相談_深雪.txt"),
            (1012, "タビ", "1012_タビ_未来と家族の幸せ相談_深雪.txt"),
            (1013, "あき", "1013_あき_定年と老後資金相談_深雪.txt"),
            (1014, "Asuka", "1014_Asuka_魂と使命の相談_深雪.txt"),
        ]
        for num, disp_name, fname in TARGETS:
            txt_path = SRC_DIR / fname
            out_dir = OUT_DIR / f"{num}_{disp_name}様M"
            p = generate(txt_path, out_dir)
            print(f"Generated: {p}")
