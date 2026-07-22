# 守護神鑑定書HTML作成ガイド（完全版）

このガイドでは、スピリチュアル鑑定書のHTMLを作成する手順を説明します。

## ファイル構造

各鑑定書は以下の構造で作成します：

```
kantei/
├── miyuki/
│   ├── 鑑定画像/
│   │   ├── 豊玉姫.png
│   │   ├── 久久能智神.png
│   │   ├── 大山祇神.png
│   │   └── ...（全ての守護神画像）
│   ├── 001_みわ様M/
│   │   └── index.html
│   ├── 002_大木陽子様M/
│   │   └── index.html
│   ├── 003_りーママ様M/
│   │   └── index.html
│   └── ...
```

**重要**:
- HTMLファイルは `miyuki/連番_名前様M/index.html` に配置
- 画像ファイルは全て `miyuki/鑑定画像/` に集約
- HTMLから画像へは相対パス `../鑑定画像/守護神名.png` で参照

## テンプレートファイル

**ベーステンプレート**: `002_大木陽子様M/index.html` または `003_りーママ様M/index.html`

新しい鑑定書を作成する際は、このファイルをコピーして内容を変更してください。

---

## GA4計測タグ（みゆき用・必須）

測定ID: **`G-JHLDFT6DR7`**（みゆき専用。かな側 `G-2SSQHY7CEL` とは別プロパティで完全分離）

計測できること（全イベントに `persona: 'miyuki'` を付与）:
- **ページ開いた**（誰が）… `page_open`＋ `kantei_id`（URLのフォルダ名＝連番_名前様M）
- **最後まで読んだ**… 署名 `.signature` が画面に入ったら `read_complete`
- **購入ボタンを押した**… `.cta-button` クリックで `cta_click`（STORESの決済ページへ進んだ数。決済完了ではない）

### 1. `<head>` 内（`<meta viewport>` の直後）に追加

```html
    <!-- Google tag (gtag.js) : GA4 計測 [GA4-MIYUKI] -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JHLDFT6DR7"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-JHLDFT6DR7');
    </script>
```

### 2. `</body>` の直前に追加（カスタムイベント）

```html
<!-- GA4 カスタム計測：誰が/最後まで読んだか/購入ボタン [GA4-MIYUKI] -->
<script>
(function () {
  function fire() {
    var seg = location.pathname.split('/').filter(Boolean);
    var last = decodeURIComponent(seg[seg.length - 1] || '');
    var id = /\.html?$/i.test(last) ? decodeURIComponent(seg[seg.length - 2] || 'unknown') : (last || 'unknown');
    var base = { kantei_id: id, persona: 'miyuki' };
    gtag('set', 'user_properties', { kantei_id: id, persona: 'miyuki' });
    gtag('event', 'page_open', base);

    var end = document.querySelector('.signature, .sign');
    if (end && 'IntersectionObserver' in window) {
      var done = false;
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting && !done) { done = true; gtag('event', 'read_complete', base); io.disconnect(); }
        });
      }, { threshold: 0.5 });
      io.observe(end);
    }

    document.querySelectorAll('.cta-button, .btn').forEach(function (b) {
      b.addEventListener('click', function () { gtag('event', 'cta_click', base); });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fire); else fire();
})();
</script>
```

**注意**: かな用ID `G-2SSQHY7CEL` は絶対にみゆきに入れない（プロパティを分けている意味が無くなる）。

---

## HTML完全テンプレート

### 1. ヘッダー部分（DOCTYPE～head終了まで）

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>◯◯様　守護神鑑定書</title>
    <style>
        /* 以下、CSS完全版を参照 */
    </style>
</head>
```

### 2. CSS完全版

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'YuMincho', serif;
    background: linear-gradient(135deg, #1a1a3e 0%, #0f0f2e 50%, #1a1a3e 100%);
    color: #e8e8f0;
    line-height: 1.8;
    padding: 20px;
    min-height: 100vh;
    font-size: 17px;  /* PC表示の基本フォントサイズ */
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: rgba(15, 15, 46, 0.7);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 8px 32px rgba(100, 100, 200, 0.2),
                inset 0 0 60px rgba(100, 100, 200, 0.05);
    border: 1px solid rgba(200, 200, 255, 0.1);
}

h1 {
    text-align: center;
    color: #a8b8ff;
    font-size: 2em;
    margin-bottom: 30px;
    text-shadow: 0 0 20px rgba(168, 184, 255, 0.5);
    letter-spacing: 0.1em;
}

h2 {
    color: #c8d0ff;
    font-size: 1.5em;
    margin: 40px 0 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(168, 184, 255, 0.3);
    letter-spacing: 0.05em;
}

.oracle-message {
    background: linear-gradient(135deg, rgba(60, 60, 120, 0.3), rgba(40, 40, 100, 0.3));
    border: 2px solid rgba(168, 184, 255, 0.3);
    border-radius: 15px;
    padding: 30px;
    margin: 30px 0;
    box-shadow: 0 4px 20px rgba(100, 100, 200, 0.2);
    position: relative;
}

.oracle-message::before {
    content: '';  /* ✨絵文字は削除 */
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 30px;
    background: #1a1a3e;
    padding: 0 15px;
}

.guardian-image {
    max-width: 400px;
    width: 100%;
    height: auto;
    margin: 30px auto;
    display: block;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(168, 184, 255, 0.3);
}

.oracle-message p {
    margin: 15px 0;
    text-align: center;
    font-size: 1.1em;
}

.section {
    margin: 30px 0;
    padding: 20px;
    background: rgba(30, 30, 70, 0.3);
    border-radius: 10px;
    text-align: center;
}

.emoji-header {
    font-size: 1.8em;
    margin: 40px 0 20px;
    color: #c8d0ff;
    text-align: left;
}

.guardian {
    text-align: center;
    font-size: 1.3em;
    color: #a8b8ff;
    margin: 20px 0;
    padding: 20px;
    background: rgba(168, 184, 255, 0.1);
    border-radius: 10px;
    text-shadow: 0 0 15px rgba(168, 184, 255, 0.4);
}

ul {
    list-style: none;
    margin: 20px 0;
}

ul li {
    margin: 10px 0;
    font-weight: bold;
    color: #ffd966;
    text-shadow: 0 0 10px rgba(255, 217, 102, 0.3);
}

.cta {
    background: rgba(30, 30, 70, 0.5);
    border: 1px solid rgba(168, 184, 255, 0.2);
    border-radius: 15px;
    padding: 40px 25px;  /* 左右25pxで横幅を確保 */
    margin: 40px 0;
    text-align: center;
    box-shadow: 0 4px 20px rgba(100, 100, 200, 0.2);
}

.cta h2 {
    border: none;
    margin: 20px 0;
}

.cta-button {
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
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(106, 122, 202, 0.9);
    background: linear-gradient(135deg, #5a6aaa, #7a8aca);
}

.price {
    font-size: 1.8em;
    color: #e8e8f0;
    margin: 20px 0 5px 0;
}

.original-price {
    text-decoration: line-through;
    color: #999;
    font-size: 1em;
}

.special-price {
    font-size: 2em;
    color: #ffd700;
    font-weight: bold;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    white-space: nowrap;
}

.limited-badge {
    color: #ff4444;
    font-weight: bold;
    font-size: 0.95em;
    margin: 10px 0;
}

.closing {
    text-align: center;
    margin: 40px 0;
    padding: 30px 15px;  /* 左右15pxで文字が入るように */
    background: rgba(60, 60, 120, 0.2);
    border-radius: 15px;
    font-size: 1.1em;
    line-height: 2;
}

.signature {
    text-align: right;
    font-size: 1.3em;
    color: #c8d0ff;
    margin-top: 30px;
}

@media (max-width: 768px) {
    body {
        font-size: 15px;  /* スマホ表示の基本フォントサイズ */
        padding: 10px;  /* 左右の余白を狭くして表示幅を確保 */
    }

    .container {
        padding: 20px 10px;  /* 上下20px、左右10pxで表示幅を最大化 */
    }

    h1 {
        font-size: 1.3em;
    }

    h2 {
        font-size: 1.2em;
    }

    .oracle-message,
    .section {
        padding: 15px 10px;  /* 左右10pxで1行の文字数を確保 */
    }

    .price {
        font-size: 1.5em;
    }

    .special-price {
        font-size: 1.8em;
    }

    .cta-button {
        font-size: 1.1em;
        padding: 15px 30px;
    }

    .guardian-image {
        max-width: 100%;
    }
}
```

---

## カラースキーム

**背景色:**
- メインの背景: `linear-gradient(135deg, #1a1a3e 0%, #0f0f2e 50%, #1a1a3e 100%)`
- コンテナ背景: `rgba(15, 15, 46, 0.7)`

**テキスト色:**
- 基本テキスト: `#e8e8f0`
- 見出し: `#a8b8ff`, `#c8d0ff`
- 強調テキスト（黄色）: `#ffd966`
- 強調テキスト（白っぽい）: `#f0f0ff`
- リスト項目: `#ffd966` (太字)
- 価格（ゴールド）: `#ffd700`
- 限定バッジ（赤）: `#ff4444`

**背景アクセント色（3〜4色ボックス用）:**
1. 黄色: `rgba(255, 215, 0, 0.7)` opacity: 0.3
2. 赤: `rgba(255, 69, 58, 0.7)` opacity: 0.3
3. 緑: `rgba(52, 199, 89, 0.7)` opacity: 0.3
4. 青: `rgba(0, 122, 255, 0.7)` opacity: 0.3（4項目の場合のみ）

---

## 黄色文字の使い方ガイド

鑑定書の中で特に強調したい部分に黄色文字（`#ffd966`）を使用します。具体的な文言ではなく、**パート・雰囲気**で判断してください。

**黄色文字を使う箇所（パート・雰囲気別）**:

1. ✨ **未来のビジョン・希望的な展開**
   - 例: 「彼からずっと気になっていましたと告白され〜」「両思いになり、愛されているあなたを感じられる日々が〜」
   - 守護神が見せてくれた幸せな未来の場面

2. 💫 **本質的な魅力・才能**
   - 例: 「あなたが笑うだけで、その場の空気が柔らかくなる。」
   - その人の持つ才能や魅力を端的に表現する部分

3. 🔔 **問いかけ・気づきを促す**
   - 例: 「最近、こんな感覚がありませんでしたか？」
   - 相手に気づきを促す質問形式の部分

4. 💝 **肯定・励まし・安心**
   - 例: 「安心してください。」「今感じている不安も、決して無駄ではありません。」
   - 不安を和らげ、相手を温かく肯定する雰囲気の文章

5. ⚠️ **問題点・現状の課題**
   - 例: 「本来のあなたなら、こんなことで立ち止まらない。」「心が揺らぐことで、オーラも乱れ〜」
   - 本来の姿との対比で現状の課題を指摘する部分

6. 🎯 **重要な決意・行動を促す**
   - 例: 「自分で幸せを掴みにいくと心に決めること。」「このままではいけない、流れを変えたい」
   - 決断や行動を強く促す部分

7. 🛡️ **守護・サポートの約束**
   - 例: 「あなたの背中をそっと押す力をお送りします。」
   - 守護やサポートを約束する部分

8. ⭐ **運命・必然性・転換点**
   - 例: 「偶然ではありません。」「止まっていた運命を、静かに動かし始めます。」
   - 必然性や運命の転換点を示す部分

**CSS指定**:
```html
<p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">テキスト</p>
```

### 守護神名（インラインspan）の黄色ルール

本式のように長文で守護神名が何度も登場する場合、**全部を黄色にしない**こと。
登場回数が多いと黄色が薄れて重要度が伝わらなくなる。

**黄色にして良いのは原則4箇所まで**:

1. **初登場** — 神様が初めて名乗られる場面（「その景色を見せてくださったのは、◯◯」）
2. **本質の説明** — 神様の核となる性質を語る場面（「◯◯は、〜の女神として祀られている」）
3. **キーとなる働きかけ** — その鑑定で最も重要な守護の動き（「◯◯が、あなたの想いを運んでくださっている」）
4. **重要な時節情報** — 「◯月は御神気が最も強く流れ込む月です」など、行動の節目に絡む言及

それ以外の本文中の繰り返し言及（「◯◯の御神気と〜」「◯◯が守ってくださっています」など定型句）は**普通の文字色**にする。

**例外**: パワーストーン等の商品案内で、石名や「詳細希望」など申込みコードは黄色を残してよい（商品情報として目立たせる目的）。

**インラインspan指定**:
```html
<span style="color: #ffd966;">木花咲耶姫</span>
```

---

## HTML本文構造

### 1. タイトル

```html
<body>
    <div class="container">
        <h1>◯◯様<br>守護神鑑定書</h1>
```

**重要**: タイトルは必ず改行を入れる

### 2. 神託メッセージセクション（守護神画像含む）

```html
<div class="oracle-message">
    <p style="margin-bottom: 90px;">金野様、</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">あなたを守る神様が<br>彼からずっと気になっていましたと告白され<br>二人で笑い合いながら食事をしている姿を<br>そっと見せてくれました。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">彼と両思いになり、<br>愛されているあなたを感じられる日々が<br>すぐそこまで来ています。</p>
    <p class="guardian" style="margin-bottom: 90px;">あなたを守っているのは、<br>市杵嶋姫命(いちきしまひめのみこと)。</p>
    <p>水の女神、宗像三女神の一柱です。</p>
    <img src="../鑑定画像/市杵嶋姫命.png" alt="市杵嶋姫命" class="guardian-image">
</div>
```

**黄色文字にする箇所（雰囲気で判断）**:
- ✨ **未来のビジョン**: 守護神が見せてくれた幸せな未来の場面
- 💫 **希望的な展開**: 両思いになる、愛される日々など、明るい未来を示す部分

**重要**:
- 画像は相対パス `../鑑定画像/守護神名.png` で参照
- 画像ファイル名は守護神名と完全一致させる

### 3. オーラ・本質セクション

```html
<div class="section">
    <p style="margin-bottom: 90px;">水面に映る月のような美しさと<br>深い愛情の加護を受けているので、繊細で純粋、<br>愛されるオーラを持っているんです。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">あなたが笑うだけで、<br>その場の空気が柔らかくなる。</p>
    <p style="margin-bottom: 90px;">そして、<br>彼のことを想うその一途な気持ちが、<br>あなたの魅力を何倍にも輝かせている。</p>
    <p style="margin-bottom: 90px;">これほど強い守護を受けているのに、<br>今あなたの心は揺れ、<br>オーラも少し乱れています。</p>
</div>
```

**黄色文字にする箇所（雰囲気で判断）**:
- 💝 **本質的な魅力**: その人の持つ才能や魅力を端的に表現する部分
- ✨ **肯定・励まし**: 相手を温かく肯定する雰囲気の文章

### 4. なぜ今、流れが滞っているのか

```html
<h2 class="emoji-header">⛩️なぜ今、流れが滞っているのか</h2>
<div class="section">
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">最近、<br>こんな感覚がありませんでしたか？</p>
    <p style="margin-bottom: 90px;">このままでいいのかという不安が消えない。<br>彼に嫌われたくないと思うほど、<br>何も言えなくなってしまう。</p>
    <p style="margin-bottom: 90px;">進んでいいのか、待つべきなのか、<br>答えが分からず、心が落ち着かない。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">本来のあなたなら、<br>こんなことで立ち止まらない。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">そして、心が揺らぐことで、<br>オーラも乱れ、<br>守護の力も届きにくくなっています。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">安心してください。</p>
</div>
```

**黄色文字にする箇所（雰囲気で判断）**:
- 🔔 **問いかけ**: 気づきを促す質問形式の部分
- 💫 **本質の指摘**: 「本来のあなたなら」など、本来の姿を示す部分
- ⚠️ **問題点の指摘**: オーラの乱れなど、現状の課題を示す部分
- 💝 **安心・励まし**: 不安を和らげる肯定的なメッセージ

### 5. ここから先の流れ

```html
<h2 class="emoji-header">⛩️ここから先の流れ</h2>
<div class="section">
    <p style="margin-bottom: 90px;">このまま問題を放っておけば<br>今までと同じように<br>不安を抱え、迷い、立ち止まりながら<br>毎日を過ごすことになります。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">あとは自分を整えて待つだけで望む未来がやってきます。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">自分で幸せを掴みにいくと<br>心に決めること。</p>
</div>
```

**黄色文字にする箇所（雰囲気で判断）**:
- 🎯 **重要な決意・行動**: 自分で幸せを掴む、心に決めるなど行動を促す部分
- ✨ **希望的な展開**: 望む未来がやってくるなど、明るい結果を示す部分

### 6. 本式守護鑑定（導入）

```html
<h2 class="emoji-header">⛩️本式守護鑑定</h2>
<div class="section">
    <p style="margin-bottom: 90px;">ここまでの鑑定で、<br>あなたを守る神様の存在と、<br>今なぜ流れが<br>滞っているのかをお伝えしました。</p>
    <p style="margin-bottom: 90px;">でも、本当に大切なのはここから。<br>あなたが理想の未来を手に入れるために<br>以下の事を霊視して、お伝えします。</p>
</div>
```

### 7. 本式守護鑑定でお伝えすること（3色ボックス）

```html
<div style="padding: 40px 0; margin: 40px 0;">
    <div style="margin: 30px 0; text-align: center;">
        <!-- 項目1: 黄色背景 -->
        <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255, 215, 0, 0.7); opacity: 0.3;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ 彼の本当の気持ち</h3>
                <p>今、彼があなたをどう思っているのか。<br>言葉にしていない本音を視ます。</p>
            </div>
        </div>

        <!-- 項目2: 赤背景 -->
        <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255, 69, 58, 0.7); opacity: 0.3;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ 二人の関係が動く時期</h3>
                <p>流れが変わるタイミングと、<br>その時あなたがすべきことをお伝えします。</p>
            </div>
        </div>

        <!-- 項目3: 緑背景 -->
        <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(52, 199, 89, 0.7); opacity: 0.3;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ 愛される流れを<br>引き寄せる方法</h3>
                <p>あなたのオーラを整え、<br>彼の心を開く具体的な方法をお伝えします。</p>
            </div>
        </div>
    </div>

    <p style="margin-top: 90px; margin-bottom: 90px; text-align: center; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">あなたの背中を<br>そっと押す力をお送りします。</p>
</div>
```

**黄色文字にする箇所（雰囲気で判断）**:
- 🛡️ **守護・サポートの約束**: 「背中をそっと押す力をお送りします」など、守護やサポートを約束する部分

**注意**: 鑑定内容によって項目数は変わる（3項目または4項目）

**重要**:
- 項目は黄・赤・緑（・青）の順
- `margin-bottom: 0` で隙間なく配置
- 角は四角（border-radiusなし）

### 8. 購入CTAセクション

```html
<div class="cta">
    <h2>【運命が動く24時間】</h2>

    <p style="margin-bottom: 90px;">今、<br>あなたを守る存在の気配が、<br>いつもより強く近くにあります。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">偶然ではありません。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">このままではいけない、<br>流れを変えたい、</p>
    <p style="margin-bottom: 90px;">ここから24時間。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">止まっていた運命を、<br>静かに動かし始めます。</p>
    <p style="margin-bottom: 90px;">進むべき道を知りたい。<br><br>そう感じた方だけ、<br>この先へ進んでください。</p>

    <div class="price">
        <span class="original-price">通常9,800円</span><br>
        <span class="limited-badge">24時間限定の特別価格</span><br>
        <span class="special-price">4,980円</span>
    </div>

    <a href="https://lnuwhrs3tncycy5pf0r3.stores.jp/items/69eb763d23b5d0e88f9854e9" class="cta-button" target="_blank">本式守護鑑定を受ける▼</a>

    <p style="margin-top: 90px;">お申し込み後、<br>購入時のお名前をお知らせください。<br>1日以内に、<br>あなただけの鑑定書をお届けします。</p>
</div>
```

**黄色文字にする箇所（雰囲気で判断）**:
- ⭐ **運命・必然性**: 「偶然ではありません」など、必然性を示す部分
- 🎯 **決意・転換点**: 「このままではいけない、流れを変えたい」など、決断を促す部分
- ✨ **運命の転換**: 「止まっていた運命を静かに動かし始めます」など、転換点を示す部分

**重要**:
- 価格は`.special-price`でゴールド
- 限定バッジは`.limited-badge`で赤

### 9. クロージングセクション

```html
<div class="closing">
    <p style="margin-bottom: 90px;">私には視えています。</p>
    <p style="margin-bottom: 90px;">彼と結ばれて、<br>愛されているあなたの姿を。</p>
    <p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">今感じている不安も、<br>決して無駄ではありません。</p>
    <p style="margin-bottom: 90px;">その未来へ続く扉を、<br>私は守護の声を受け取りながら、<br>丁寧に開いていきますね。</p>

    <div class="signature">深雪</div>
</div>

    </div>
</body>
</html>
```

**黄色文字にする箇所（雰囲気で判断）**:
- 💝 **肯定・励まし**: 「今感じている不安も、決して無駄ではありません」など、不安を肯定し励ます部分

**重要**:
- 署名は必ず「深雪」（テキストが深幸でも変更する）

---

## 作成手順

1. **テンプレートをコピー**
   ```bash
   cp miyuki/002_大木陽子様M/index.html miyuki/XXX_名前様M/index.html
   ```

2. **テキストファイルを読む**
   - 元のテキストファイルから内容を確認

3. **以下を置き換え**
   - タイトルの名前
   - 守護神名と説明
   - 画像パス（守護神名）
   - オーラの色・説明
   - お悩み内容
   - リスト項目
   - ビジョン内容
   - 署名（深雪に統一）

4. **改行とmargin-bottomを確認**
   - 段落間は`<p>`で分ける
   - 段落内は`<br>`で改行
   - 基本的に`margin-bottom: 90px`を使用（3改行相当）
   - **改行は元のテキストに合わせる**（独自に改行を追加・変更しない）

5. **強調箇所を確認**
   - **黄色文字**: 上記「黄色文字の使い方ガイド」を参照し、雰囲気・パートで判断
     - 未来のビジョン、本質の魅力、問いかけ、励まし、問題点、決意促進、守護の約束、運命の転換点など
   - **白強調**: 特に重要な問いかけや呼びかけ（使用頻度は低め）
   - タイトルは必ず改行: `◯◯様<br>守護神鑑定書`

---

## チェックリスト

作成完了後、以下を確認：

- [ ] フォルダ名が`miyuki/連番_名前様M/`形式になっている
- [ ] HTMLファイル名が`index.html`になっている
- [ ] タイトルが`◯◯様<br>守護神鑑定書`形式で改行が入っている
- [ ] 守護神名が正しく設定されている
- [ ] 画像パスが`../鑑定画像/守護神名.png`になっている
- [ ] oracle-message::beforeが`content: ''`になっている（✨なし）
- [ ] bodyに`font-size: 17px`が設定されている（PC表示）
- [ ] スマホ用メディアクエリで`font-size: 15px`が設定されている
- [ ] 段落の`margin-bottom`が基本的に`90px`になっている（3改行相当）
- [ ] ctaのpaddingが`40px 25px`になっている
- [ ] closingのpaddingが`30px 15px`になっている
- [ ] スマホ用メディアクエリでctaのpaddingが`40px 15px`になっている
- [ ] スマホ用メディアクエリでclosingのpaddingが`30px 10px`になっている
- [ ] 色付きボックスの項目数が正しい（3項目または4項目）
- [ ] 色付きボックスが黄・赤・緑（・青）の順で配置されている
- [ ] 色付きボックスのmargin-bottomが0になっている（隙間なし）
- [ ] STORES URLが`https://lnuwhrs3tncycy5pf0r3.stores.jp/items/69eb763d23b5d0e88f9854e9`になっている
- [ ] 黄色強調すべき箇所（未来のビジョン、本質の魅力、問いかけ、励まし、問題点、決意促進、守護の約束、運命の転換点など）が正しく強調されている
- [ ] 署名が「深雪」になっている

---

## よく使うスタイルパターン集

### 段落（通常）
```html
<p style="margin-bottom: 90px;">テキスト</p>
```

### 段落（強調・白）
```html
<p style="margin-bottom: 90px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">テキスト</p>
```

### 段落（強調・黄色）- 黄色文字の箇所に使用
```html
<p style="margin-bottom: 90px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">テキスト</p>
```

### 段落（太字のみ）- ビジョン部分に使用
```html
<p style="margin-bottom: 90px; font-weight: bold;">テキスト</p>
```

**重要**: 基本的に段落間は`margin-bottom: 90px`を使用（3改行相当）

### インラインで【本式守護鑑定】を強調
```html
<span style="font-size: 1.4em; font-weight: bold; color: #c8d0ff;">【本式守護鑑定】</span>
```

---

## トラブルシューティング

### 画像が表示されない
- パスが正しいか確認: `../鑑定画像/守護神名.png`
- ファイル名が完全一致しているか確認（大文字小文字、全角半角）

### 4色ボックスに隙間がある
- 各ボックスの`margin-bottom: 0`を確認

### 署名が深幸になっている
- 必ず「深雪」に変更する

### ✨が表示される
- CSS の `.oracle-message::before` の `content: ''` を確認

---

## 完成例

- `001_みわ様M/index.html` - 守護神: 豊玉姫
- `002_大木陽子様M/index.html` - 守護神: 久久能智神
- `003_りーママ様M/index.html` - 守護神: 大山祇神

これらをテンプレートとして参照してください。

---

## モバイル対応について

### 実装されている対応

このテンプレートはスマートフォンで閲覧した際に最適化されるよう、以下の対応が施されています。

#### 1. 価格表示の改行防止

**問題**: スマホで「4980円」が「4980」と「円」に分かれて表示される

**解決策**: `.special-price` クラスに `white-space: nowrap` を追加

```css
.special-price {
    font-size: 2em;
    color: #ffd700;
    font-weight: bold;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    white-space: nowrap;  /* 重要: 価格を改行させない */
}
```

#### 2. 横幅の最適化（重要）

**問題**: スマホでパディングが多すぎて、1行に表示できる文字数が少なくなり、変な位置で自動改行が発生する

**解決策**: メディアクエリ内で左右のパディングを10pxに縮小し、表示幅を最大化

```css
@media (max-width: 768px) {
    body {
        font-size: 15px;  /* スマホ表示の基本フォントサイズ */
        padding: 10px;  /* 重要: 左右の余白を10pxに */
    }

    .container {
        padding: 20px 10px;  /* 重要: 左右10pxで表示幅を確保 */
    }

    .oracle-message,
    .section {
        padding: 15px 10px;  /* 重要: 左右10pxで1行の文字数を確保 */
    }

    .cta {
        padding: 40px 15px;  /* CTAカードも左右を狭く */
    }

    .closing {
        padding: 30px 10px;  /* クロージングも左右を狭く */
    }
}
```


#### 3. フォントサイズの最適化

**基本フォントサイズ**:
- PC表示: `font-size: 17px` (bodyに設定)
- スマホ表示: `font-size: 15px` (メディアクエリ内のbodyに設定)

**解決策**: メディアクエリ内で全体的にフォントサイズを調整

```css
@media (max-width: 768px) {
    h1 {
        font-size: 1.3em;  /* タイトルサイズ調整 */
    }

    h2 {
        font-size: 1.1em;  /* 見出しサイズ調整 */
    }

    .emoji-header {
        font-size: 1.3em;  /* 絵文字ヘッダーサイズ調整 */
    }

    .oracle-message p {
        font-size: 1em;  /* オーラクルメッセージ調整 */
    }

    .guardian {
        font-size: 1.1em;  /* 守護神名調整 */
        padding: 15px;
    }

    .price {
        font-size: 1.5em;  /* 通常価格サイズ調整 */
    }

    .special-price {
        font-size: 1.8em;  /* 特別価格サイズ調整 */
    }

    .cta-button {
        font-size: 1.1em;  /* ボタンテキストサイズ調整 */
        padding: 15px 30px;  /* ボタンパディング調整 */
    }

    .guardian-image {
        max-width: 100%;  /* 画像が横幅に収まるように */
    }
}
```


## 重要なポイントまとめ

### フォントサイズ
- **PC**: `font-size: 17px` (bodyに設定)
- **スマホ**: `font-size: 15px` (メディアクエリ内)
- 本式守護鑑定のタイトル: `1.3em`（1.5emから変更）

### 横幅・padding
- **PC**:
  - cta: `padding: 40px 25px`
  - closing: `padding: 30px 15px`
- **スマホ**:
  - body, container, oracle-message, section: 左右`10px`
  - cta: `padding: 40px 15px`
  - closing: `padding: 30px 10px`

---

## 装飾・アニメーション（標準オプション）

鑑定書をリッチに見せるため、以下の3つの動きを標準で入れます。
**世界観を壊さない範囲で効果が高いもの**だけに絞っています。

1. **スクロールフェードイン** — 各セクションが視界に入ったときにふわっと現れる
2. **守護神画像の呼吸する光輪** — 神様の性質に合わせた色で box-shadow が脈動
3. **CTAボタンの脈動** — ボタンが常時うっすら膨らんで目線が止まる

### 1. CSS追記（`<style>`内、メディアクエリの直前に追加）

```css
/* 守護神の光輪カラー（神様によって書き換える） */
:root {
    --aura-color-1: 255, 180, 100;  /* 内側の光 */
    --aura-color-2: 255, 120, 60;   /* 外側の光 */
}

/* スクロールフェードイン */
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 1.2s ease-out, transform 1.2s ease-out;
}
.reveal.is-visible {
    opacity: 1;
    transform: translateY(0);
}

/* 守護神画像の光輪（呼吸する炎） */
.guardian-image {
    position: relative;
    animation: aura-breath 4s ease-in-out infinite;
}
@keyframes aura-breath {
    0%, 100% {
        box-shadow:
            0 0 30px rgba(var(--aura-color-1), 0.35),
            0 0 60px rgba(var(--aura-color-2), 0.2),
            0 4px 20px rgba(168, 184, 255, 0.3);
    }
    50% {
        box-shadow:
            0 0 50px rgba(var(--aura-color-1), 0.6),
            0 0 100px rgba(var(--aura-color-2), 0.35),
            0 4px 20px rgba(168, 184, 255, 0.3);
    }
}

/* CTAボタンの脈動 */
.cta-button {
    animation: pulse 2.4s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        box-shadow: 0 6px 25px rgba(74, 90, 154, 0.7);
    }
    50% {
        transform: scale(1.035);
        box-shadow: 0 8px 35px rgba(168, 184, 255, 0.9), 0 0 40px rgba(168, 184, 255, 0.4);
    }
}
.cta-button:hover {
    animation: none;
}
```

### 2. HTML側で `reveal` クラスを付ける

フェードイン対象にしたい要素に `reveal` クラスを足します。

- `<div class="oracle-message reveal">`
- `<div class="section reveal">`（複数箇所すべて）
- `<div class="cta reveal">`
- `<div class="closing reveal">`
- 色付きボックス（3〜4色ボックス）の各 `<div>` にも `reveal`

### 3. JS追記（`</body>` の直前に追加）

```html
<script>
    (function () {
        var els = document.querySelectorAll('.reveal');
        if (!('IntersectionObserver' in window)) {
            els.forEach(function (el) { el.classList.add('is-visible'); });
            return;
        }
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) {
                    e.target.classList.add('is-visible');
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
        els.forEach(function (el) { io.observe(el); });
    })();
</script>
```

---

## 守護神 × 光輪カラー プリセット

`:root` の `--aura-color-1` `--aura-color-2` を、守護神に合わせて書き換えてください。

| 系統 | 内側 (--aura-color-1) | 外側 (--aura-color-2) | 該当する神様 |
|---|---|---|---|
| 火・橙 | `255, 180, 100` | `255, 120, 60` | 火産霊神、奥津日子命、迦楼羅天 |
| 火・赤 | `255, 140, 90` | `230, 80, 50` | 火之迦具土神、三宝荒神 |
| 火・赤深 | `255, 120, 80` | `210, 60, 40` | 不動明王 |
| 水・青 | `120, 200, 255` | `60, 140, 220` | 豊玉姫、市杵嶋姫命、住吉大神 |
| 海・深青 | `90, 160, 220` | `40, 100, 180` | 綿津見神 |
| 水・桃青 | `170, 200, 255` | `110, 150, 220` | 弁財天 |
| 浄化水 | `180, 220, 255` | `100, 170, 230` | 瀬織津姫、罔象女神、弥都波能売神、速秋津日子・比売神 |
| 深水・龍 | `110, 150, 210` | `60, 100, 170` | 闇淤加美神、高淤加美神 |
| 龍・青紫 | `160, 180, 240` | `110, 130, 210` | 龍樹菩薩 |
| 木・緑 | `180, 230, 150` | `120, 180, 90` | 久久能智神、五十猛命、木俣神 |
| 草・緑 | `200, 230, 160` | `140, 190, 100` | 鹿屋野比売 |
| 山・深緑 | `150, 200, 140` | `90, 150, 80` | 大山祇神 |
| 雪山・銀緑 | `230, 240, 230` | `180, 210, 180` | 白山比咩神 |
| 花・桃 | `255, 180, 210` | `230, 130, 180` | 木花咲耶姫 |
| 福・桃 | `255, 200, 220` | `230, 150, 200` | 吉祥天 |
| 土・茶 | `220, 180, 140` | `180, 130, 80` | 埴山姫神、埴山彦神、大地主神 |
| 神鹿・茶金 | `230, 200, 150` | `190, 150, 90` | 春日大明神 |
| 金・銀金 | `240, 220, 160` | `200, 170, 100` | 金山姫神、金山彦神 |
| 武・金緑 | `230, 210, 140` | `180, 160, 80` | 毘沙門天 |
| 剣・白銀 | `220, 230, 240` | `170, 180, 200` | 布都御魂、経津主神 |
| 武・銀 | `210, 225, 240` | `160, 180, 210` | 日本武尊 |
| 雷・紫 | `200, 170, 255` | `150, 100, 220` | 建御雷神 |
| 太陽・金 | `255, 230, 130` | `255, 180, 80` | 天照大御神 |
| 稲・黄金 | `255, 220, 140` | `230, 170, 80` | 宇迦之御魂神 |
| 穀・黄金 | `255, 225, 150` | `230, 180, 90` | 豊受大神 |
| 狐・橙金 | `255, 200, 120` | `230, 160, 70` | 吒枳尼天 |
| 大地・縁 | `180, 210, 130` | `130, 170, 80` | 大己貴命 |
| 道・黄橙 | `255, 200, 100` | `230, 150, 50` | 猿田彦命 |
| 中央・白紫 | `230, 220, 255` | `190, 180, 230` | 天之御中主神 |
| 創造・白紫 | `240, 230, 255` | `200, 190, 235` | 高御産巣日神 |

---

## 背景演出（応用オプション：元素→神様→扉のクロスフェード）

標準の3点セット（フェードイン/光輪/CTA脈動）に加えて、画面いっぱいの背景画像をスクロールに合わせて切り替える演出。世界観をより没入させたい鑑定書で使う。

**流れ（3段階）：**
1. 冒頭〜守護神登場まで＝鑑定対象者の**日干（十干）に対応する元素画像**
2. 守護神登場〜本式4メニューの手前まで＝**守護神の画像**
3. 本式4メニュー以降〜結びまで＝**扉2.jpg**（「運命の扉」の演出と対応）

背景はすべて `position: fixed` で画面全体に敷き、スクロール位置に応じて opacity をクロスフェード。文字の可読性を保つため、背景レイヤーの上に暗いグラデーションの `.deity-veil` を常時重ねる。

### 1. CSS追記（`<style>`内、メディアクエリの直前に追加）

```css
/* ===== 演出：元素の背景（冒頭〜神様登場まで） ===== */
.element-bg {
    position: fixed;
    inset: 0;
    z-index: -4;
    background-image: url("../鑑定画像/【元素画像プリセット表から選択】");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    filter: blur(1.5px) brightness(0.85);
    opacity: 0.4;
    pointer-events: none;
    transition: opacity 1.4s ease;
}
.element-bg.is-hidden { opacity: 0; }

/* ===== 演出：神様の背景（神様登場〜本式4メニューの手前まで） ===== */
.deity-bg {
    position: fixed;
    inset: 0;
    z-index: -3;
    background-image: url("../鑑定画像/【守護神画像】");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center 18%;
    filter: blur(1.5px) brightness(0.85);
    opacity: 0;
    pointer-events: none;
    transition: opacity 1.4s ease;
}
.deity-bg.is-visible { opacity: 0.4; }

/* ===== 演出：本式4メニュー〜クロージングは扉の背景に続ける ===== */
.door-bg {
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
}
.door-bg.is-visible { opacity: 0.4; }

.deity-veil {
    position: fixed;
    inset: 0;
    z-index: -2;
    pointer-events: none;
    background:
        radial-gradient(ellipse at 50% 20%, rgba(15, 15, 46, 0.15) 0%, rgba(15, 15, 46, 0.55) 60%, rgba(15, 15, 46, 0.85) 100%),
        linear-gradient(180deg, rgba(15, 15, 46, 0.25) 0%, rgba(15, 15, 46, 0.7) 100%);
}
```

深海（壬水）だけは元画像が暗すぎて既存の背景色に埋もれるため、使う場合は `filter: blur(1.5px) brightness(1.5) contrast(1.2);` に差し替え、opacityも0.6程度まで上げる。

### 2. HTML側の配置

body直下、`.aurora` より前に4つのdivを追加（`.container` の外）：

```html
<div class="element-bg" id="elementBg"></div>
<div class="deity-bg" id="deityBg"></div>
<div class="door-bg" id="doorBg"></div>
<div class="deity-veil"></div>
```

本文中に、切り替えタイミングを示す目印（sentinel）を2つ埋め込む：

- 守護神の名前が**最初に明かされる直前**（「あなたを守っているのは◯◯神」の段落の直前）に `<div id="guardianSentinel"></div>`
- 本式4メニュー（3〜4色ボックス）の**直前**（その手前の `.section` の直後）に `<div id="deitySentinel"></div>`

### 3. JS追記（`</body>` の直前に追加）

```html
<script>
(function () {
    var elementBg = document.getElementById('elementBg');
    var deityBg = document.getElementById('deityBg');
    var doorBg = document.getElementById('doorBg');
    var guardianSentinel = document.getElementById('guardianSentinel');
    var deitySentinel = document.getElementById('deitySentinel');
    if (!elementBg || !deityBg || !doorBg || !guardianSentinel || !deitySentinel) return;

    var layers = [elementBg, deityBg, doorBg];
    function show(active) {
        layers.forEach(function (el) {
            if (el === active) el.classList.add('is-visible');
            else el.classList.remove('is-visible');
        });
        elementBg.classList.toggle('is-hidden', active !== elementBg);
    }

    function onScroll() {
        var trigger = window.innerHeight * 0.65;
        var guardianReached = guardianSentinel.getBoundingClientRect().top < trigger;
        var doorReached = deitySentinel.getBoundingClientRect().top < trigger;

        if (!guardianReached) {
            show(elementBg);
        } else if (!doorReached) {
            show(deityBg);
        } else {
            show(doorBg);
        }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
})();
</script>
```

### 元素背景プリセット（十干 × 画像）

背景に使う元素画像は、**鑑定対象者本人の日干（十干）**で選ぶ（守護神から逆引きしない。同じ神様でも人によって対応する十干が違うため）。画像はすべて `miyuki/鑑定画像/` にある。

| 十干 | 画像ファイル | 該当する神様（参考・命式ガイドの神様リファレンスと対応） |
|---|---|---|
| 甲木 | 深い森.jpg | 五十猛命、久久能智神、大山祇神、春日大明神 |
| 乙木 | 若葉.jpg | 木花咲耶姫、鹿屋野比売、豊受大神、木俣神、弁財天 |
| 丙火 | 太陽.gif | 天照大御神、火之迦具土神、天之御中主神、高御産巣日神、日本武尊 |
| 丁火 | ろうそく.jpg | 火産霊神、奥津日子命、三宝荒神、迦楼羅天、不動明王 |
| 戊土 | 大地.jpg | 大山祇神、大己貴命、埴山彦神、猿田彦命、毘沙門天 |
| 己土 | 肥沃な大地.webp | 埴山姫神、豊受大神、宇迦之御魂神、大地主神、吒枳尼天 |
| 庚金 | 刀.png | 建御雷神、経津主神、布都御魂、金山彦神、不動明王 |
| 辛金 | 宝石.jpg | 市杵嶋姫命、瀬織津姫、白山比咩神、金山姫神、吉祥天 |
| 壬水 | 深海.jpg（暗いのでbrightness/contrast調整推奨） | 綿津見神、住吉大神、豊玉姫、速秋津日子・比売神、弁財天 |
| 癸水 | 水面.jpg | 罔象女神、闇淤加美神、高淤加美神、弥都波能売神、龍樹菩薩 |

---

## 本式（有料）鑑定書での背景演出（拡張パターン）

無料鑑定（M）は元素→神様→扉の3段階だが、本式は文章が長く節目（今後の流れの各時期、パワーストーン紹介、結びなど）が多いため、同じ仕組みを以下のように拡張する。

**無料鑑定パターンとの違い：**

1. **sentinel↔背景の対応を配列化し、if-elseの連鎖ではなく「一番下まで見て、最後に到達したsentinelの背景を表示する」ループ処理にする。** sentinelが増えても配列に1行足すだけで済む。
2. **セクションごとに専用の背景レイヤーを追加できる。** 例：「今後の流れ」の各時期に季節画像（冬/夏/秋/冬/夏/春など、暦の季節に合わせて割り当て）、「パワーストーン」セクションに石のブレスレット画像。同じ画像を複数のsentinelから使い回してよい（無料鑑定でelementBgを2箇所で使い回すのと同じ考え方）。
3. **元の背景（神様や扉）に途中で戻したい場合は、そのdivをstages配列に再度登録するだけでよい**（新しいdivを作る必要はない）。例：パワーストーン紹介の直前に「神様」に戻す、結びの直前に「扉」に戻す、など。
4. **`.deity-veil`の不透明度は、本式では以下の値まで下げる。** レイヤー数が増え、各背景写真がopacity 0.4程度でも埋もれやすくなるため（無料鑑定の初期値 radial `0.15/0.55/0.85`、linear `0.25/0.7` より大幅に薄い）。

```css
.deity-veil {
    background:
        radial-gradient(ellipse at 50% 20%, rgba(15, 15, 46, 0.04) 0%, rgba(15, 15, 46, 0.15) 60%, rgba(15, 15, 46, 0.25) 100%),
        linear-gradient(180deg, rgba(15, 15, 46, 0.06) 0%, rgba(15, 15, 46, 0.18) 100%);
}
```

**JSパターン（配列＋ループで拡張）：**

```js
(function () {
    var elementBg = document.getElementById('elementBg');
    var deityBg = document.getElementById('deityBg');
    var doorBg = document.getElementById('doorBg');
    // セクション専用の背景レイヤーもここで取得（例：季節・パワーストーンなど）

    var stages = [
        { el: document.getElementById('elementSentinel'), bg: elementBg },
        { el: document.getElementById('guardianSentinel'), bg: deityBg },
        { el: document.getElementById('essenceSentinel'), bg: elementBg },
        { el: document.getElementById('deitySentinel'), bg: doorBg },
        // ここから先、セクションごとにsentinelと背景を追加していく
        { el: document.getElementById('guardianReturnSentinel'), bg: deityBg }, // 例：途中で神様に戻す
        { el: document.getElementById('closingSentinel'), bg: doorBg }          // 例：結びの直前で扉に戻す
    ].filter(function (stage) { return !!stage.el; });
    if (!stages.length) return;

    var layers = [elementBg, deityBg, doorBg /* , 追加した背景レイヤーも全部ここに列挙 */];
    function show(active) {
        layers.forEach(function (el) {
            if (el === active) el.classList.add('is-visible');
            else el.classList.remove('is-visible');
        });
    }

    function onScroll() {
        var trigger = window.innerHeight * 0.65;
        var active = null;
        for (var i = 0; i < stages.length; i++) {
            if (stages[i].el.getBoundingClientRect().top < trigger) {
                active = stages[i].bg;
            }
        }
        show(active);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
})();
```

**完成例:** `961_荒川理恵様_本式守護鑑定/index.html` を参照してください。季節背景（今後の流れ）、パワーストーン背景、神様⇄扉の複数回切り替え、deity-veilの薄め調整など、この拡張パターンの実装例として最も詳しく作り込まれています。**本式のHTMLを新規作成する際は、まずこのファイルの構成を参考にしてください。**

---

## 花びら演出（応用オプション：オーラカラーの花びらが舞う）

背景クロスフェードに加えて、画面全体に花びらが常時舞う演出。色は**きらきら（白い光の粒）ではなく、守護神の光輪カラー（オーラ）と同じ色**を使う。世界観を統一するため、独自の色を当てずに「守護神 × 光輪カラー プリセット」表の値をそのまま流用する。

### 1. CSS追記（`<style>`内）

```css
/* ===== 演出：花びら ===== */
#petals {
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
}
```

body直下、`.deity-veil` の直後に追加：

```html
<canvas id="petals"></canvas>
```

### 2. JS追記（`</body>` の直前、背景クロスフェードのIIFEの後ろに追加）

```html
<script>
/* ===== 演出：花びら ===== */
(function () {
    var cv = document.getElementById('petals');
    var ctx = cv.getContext('2d');
    var W, H, dpr = Math.min(window.devicePixelRatio || 1, 2);
    var isMobile = window.innerWidth < 700;

    function resize() {
        W = window.innerWidth; H = window.innerHeight;
        cv.width = W * dpr; cv.height = H * dpr;
        cv.style.width = W + 'px'; cv.style.height = H + 'px';
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    window.addEventListener('resize', resize);

    var petals = [];
    var petalN = isMobile ? 14 : 24;
    for (var i = 0; i < petalN; i++) {
        petals.push({
            x: Math.random() * W,
            y: Math.random() * H,
            s: 5 + Math.random() * 7,
            vy: 0.35 + Math.random() * 0.7,
            sway: Math.random() * Math.PI * 2,
            swayV: 0.008 + Math.random() * 0.014,
            rot: Math.random() * Math.PI * 2,
            rotV: (Math.random() - 0.5) * 0.03,
            hue: Math.random() < 0.6 ? 'light' : 'deep'
        });
    }
    function drawPetal(p) {
        ctx.save();
        ctx.translate(p.x + Math.sin(p.sway) * 26, p.y);
        ctx.rotate(p.rot);
        var g = ctx.createRadialGradient(0, 0, 0, 0, 0, p.s);
        if (p.hue === 'light') {
            g.addColorStop(0, 'rgba(【光輪カラー内側】, 0.95)');
            g.addColorStop(1, 'rgba(【光輪カラー内側】, 0.25)');
        } else {
            g.addColorStop(0, 'rgba(【光輪カラー外側】, 0.95)');
            g.addColorStop(1, 'rgba(【光輪カラー外側】, 0.25)');
        }
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.ellipse(0, 0, p.s, p.s * 0.62, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    function tick() {
        ctx.clearRect(0, 0, W, H);
        for (var pi = 0; pi < petals.length; pi++) {
            var p = petals[pi];
            p.y += p.vy;
            p.sway += p.swayV;
            p.rot += p.rotV;
            if (p.y > H + 20) { p.y = -20; p.x = Math.random() * W; }
            drawPetal(p);
        }
        requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
})();
</script>
```

**色の決め方（重要）**: `【光輪カラー内側】`/`【光輪カラー外側】`には、その鑑定書の守護神に対応する「守護神 × 光輪カラー プリセット」表の `--aura-color-1`（内側）/`--aura-color-2`（外側）の数値をそのまま入れる。例：961（大山祇神・山・深緑）では `150, 200, 140`（内側）/ `90, 150, 80`（外側）を使用。独自の色（きらきらの白系など）を新たに作らず、既存のオーラカラーに揃えることで世界観が統一される。

---

## 色テストパネル（作成時に色を試したいとき・本番ではコメントアウト推奨）

新規作成時に「この神様にはどの色が合うか」を試したい場合、ページ上部に色見本パネルを設置できます。
完成時はパネル部分（HTMLの `<div class="color-test-panel">` ブロックとJSの `buildPalette` 関数）を削除してください。

参考実装は `688_ゆうこ様M copy/index.html` を参照。