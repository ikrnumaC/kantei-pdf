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

---

## HTML本文構造

### 1. タイトル

```html
<body>
    <div class="container">
        <h1>【名前】様<br>守護神鑑定書</h1>
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

   **改行の処理フロー**:
   1. まず全文を<br>なしで並べる
   2. 読みやすい長さ（12〜15文字程度）になるよう、読点(、)や助詞の後で改行を入れる

   **例**:
   ```html
   <!-- ❌ ダメ: 無駄に細切れ -->
   <p style="margin-bottom: 90px;">力強く、<br>どっしりとした<br>生命力を<br>持っています。</p>

   <!-- ⭕ 良い: 適切な長さで改行 -->
   <p style="margin-bottom: 90px;">力強く、どっしりとした<br>生命力を持っています。</p>
   <!-- 「力強く、どっしりとした」(13文字) + 「生命力を持っています。」(12文字) -->
   ```

5. **強調箇所を確認**
   - **黄色文字**: 上記「黄色文字の使い方ガイド」を参照し、雰囲気・パートで判断
     - 未来のビジョン、本質の魅力、問いかけ、励まし、問題点、決意促進、守護の約束、運命の転換点など
   - **白強調**: 特に重要な問いかけや呼びかけ（使用頻度は低め）
   - タイトルは必ず改行: `【名前】様<br>守護神鑑定書`

---

## チェックリスト

作成完了後、以下を確認：

- [ ] フォルダ名が`miyuki/連番_名前様M/`形式になっている
- [ ] HTMLファイル名が`index.html`になっている
- [ ] タイトルが`【名前】様<br>守護神鑑定書`形式で改行が入っている
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