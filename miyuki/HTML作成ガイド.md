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
    <title>【名前】様　守護神鑑定書</title>
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

**背景アクセント色（4つの項目用）:**
1. 黄色: `rgba(255, 215, 0, 0.7)` opacity: 0.3
2. 赤: `rgba(255, 69, 58, 0.7)` opacity: 0.3
3. 緑: `rgba(52, 199, 89, 0.7)` opacity: 0.3
4. 青: `rgba(0, 122, 255, 0.7)` opacity: 0.3

---

## HTML本文構造

### 1. タイトル

```html
<body>
    <div class="container">
        <h1>【名前】様　守護神鑑定書</h1>
```

### 2. 神託メッセージセクション（守護神画像含む）

```html
<div class="oracle-message">
    <p style="margin-bottom: 30px;">りーママ様、</p>
    <p style="margin-bottom: 30px;">視えました。</p>
    <p class="guardian" style="margin-bottom: 30px;">あなたを守っているのは、<br>大山祇神(おおやまつみのかみ)。</p>
    <p>山を司る偉大な神様です。</p>
    <img src="../鑑定画像/大山祇神.png" alt="大山祇神" class="guardian-image">
</div>
```

**重要**:
- 画像は相対パス `../鑑定画像/守護神名.png` で参照
- 画像ファイル名は守護神名と完全一致させる
- 守護神名と読み仮名は1行にまとめる（20文字以内）

### 3. オーラ・本質セクション

```html
<div class="section">
    <p style="margin-bottom: 30px;">あなたのオーラは、深い森の緑。<br>力強く、どっしりとした生命力を<br>持っています。</p>
    <p style="margin-bottom: 30px;">大山祇神に守られる人は、<br>どっしりと構えた大きな器を持ち、<br>周囲を守る力がある頼られる存在。</p>
    <p style="margin-bottom: 30px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">家族を包み込む、揺るがない愛。<br>それがあなたの本質です。</p>
    <p style="margin-bottom: 30px;">これほど強い守護神に<br>守られているのに、今、<br>流れが悪くなっている…</p>
    <p>その原因をお伝えします。</p>
</div>
```

**重要**: 本質の部分は必ず黄色強調にする、20文字ルールに従う

### 4. お悩みセクション

```html
<h2 class="emoji-header">⛩️お悩みについて</h2>
<div class="section">
    <p style="margin-bottom: 30px;">【お悩みの内容】</p>
    <p style="margin-bottom: 30px;">【現状の説明】</p>
    <p style="margin-bottom: 30px;">この問題は、実はあなたが<br>悪いわけではありません。</p>
    <p style="font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">オーラを整え、守護神からのエネルギーを<br>正しく受け取れば、お金の流れも、<br>お子さんとの関係も、精神状態も、<br>必ず変わります。</p>
</div>
```

**重要**:
- 最後の段落は必ず白強調にする
- 「オーラを整え〜」の部分は20文字ルールに従って改行（細切れにしない）

### 5. なぜ今、悪いものを引き寄せているのか

```html
<h2 class="emoji-header">⛩️なぜ今、<br>　悪いものを引き寄せているのか</h2>
<div class="section">
    <p style="margin-bottom: 20px;">去年の秋。<br>こんなことがありませんでしたか?</p>
    <ul style="margin-bottom: 30px;">
        <li>頑張っているのに、<br>報われない気がして<br>焦りが強くなった</li>
        <li>周囲に頼れず、<br>一人で抱え込んで孤独を感じた</li>
        <li>前向きになれず、<br>心から笑えない日が続いた</li>
    </ul>
    <p style="margin-bottom: 30px;">それらは、守護神の力が弱まり、<br>あなたを守るオーラが<br>少なくなってしまったことで<br>起こっているのです。</p>
    <p style="margin-bottom: 30px;">あなたは本来、<br>山のような包容力を持つ人。<br>家族を包み込み、<br>安心させる力がある。</p>
    <p style="margin-bottom: 30px;">これまで、あなたは家族のために<br>懸命に頑張ってきた。<br>母として、妻として、<br>しっかりと守ろうとしてきた。</p>
    <p style="margin-bottom: 30px;">でも今、守護の力が<br>弱くなってきている…</p>
    <p>だから、心に余裕を持つこともできず、<br>明るく笑うこともできず、<br>お金の流れも<br>滞ってしまっているのです。</p>
</div>
```

**重要**: リストは自動的に黄色太字になる、20文字ルールに従う

### 6. 二つの道

```html
<h2 class="emoji-header">⛩️二つの道</h2>
<div class="section">
    <p style="margin-bottom: 30px;">このまま、オーラが乱れたままだと、<br>お金の不安は消えず、<br>家族の雰囲気も暗くなり、<br>精神的に限界を迎えてしまう。<br>誰も笑えない日々が続いてしまう。</p>
    <p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">でも、ここで流れを変えたら。</p>
    <p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">オーラが整い、守護の力を<br>受け取れるようになり、<br>お金の流れが良くなり、<br>家族みんなが笑顔で食卓を囲む。<br>あなたが心から安心して、<br>穏やかに過ごせる日々が訪れる。</p>
    <p>どちらの道を歩むかは、まだ今なら、<br>あなた自身で選べます。</p>
</div>
```

**重要**: 「でも、ここで流れを変えたら。」と良い未来の部分は白強調にする、20文字ルールに従う

### 7. 守護の方法

```html
<h2 class="emoji-header">⛩️守護の方法</h2>
<div class="section">
    <p style="margin-bottom: 30px;">ここまでの鑑定で、<br>あなたの守護神とオーラの状態と、<br>なぜ今のような状況なのかを<br>お伝えしました。</p>
    <p style="margin-bottom: 30px;">でも、一番大事なのはここから、</p>
    <p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">「じゃあ、具体的にどうすれば<br>良くなるのか」<br>「理想の未来を手に入れるためには、<br>何をすればいいのか」<br>ということですよね。</p>
    <p style="margin-bottom: 30px;"><span style="font-size: 1.4em; font-weight: bold; color: #c8d0ff;">【本式守護鑑定】</span>では、<br>あなたが実際に守護を受け取るための<br>"具体的な方法"</p>
    <p>そして、未来が明るく広がるタイミングを<br>お伝えいたします。</p>
</div>
```

**重要**: 質問部分は白強調、【本式守護鑑定】は大きく強調、20文字ルールに従う

### 8. 本式守護鑑定でお伝えすること（4色ボックス）

```html
<div style="padding: 40px 0; margin: 40px 0;">
    <h2 style="text-align: center; color: #c8d0ff; font-size: 1.3em; margin-bottom: 50px; border: none; text-shadow: 0 0 20px rgba(168, 184, 255, 0.5);">🔮 本式守護鑑定でお伝えすること</h2>

    <div style="margin: 30px 0; text-align: center;">
        <!-- 項目1: 黄色背景 -->
        <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255, 215, 0, 0.7); opacity: 0.3;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ あなたの運命が動き出す転機</h3>
                <p>【説明文 - テキストから抽出】</p>
            </div>
        </div>

        <!-- 項目2: 赤背景 -->
        <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255, 69, 58, 0.7); opacity: 0.3;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ 守護神から守護を<br>受け取る方法</h3>
                <p>【説明文 - テキストから抽出】</p>
            </div>
        </div>

        <!-- 項目3: 緑背景 -->
        <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(52, 199, 89, 0.7); opacity: 0.3;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ 守護の力を手に入れた<br>あなたの未来</h3>
                <p>【説明文 - テキストから抽出】</p>
            </div>
        </div>

        <!-- 項目4: 青背景 -->
        <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 122, 255, 0.7); opacity: 0.3;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ 私の守護の力をあなたに</h3>
                <p>【説明文 - テキストから抽出】</p>
            </div>
        </div>
    </div>

    <p style="margin-top: 30px; text-align: center;">このまま方法を知らずに過ごすか、<br>守護を受け取る道を選ぶか。<br>決めるのは、あなたです。</p>
</div>
```

**注意**: 4色ボックスの各タイトルには改行が入ることがあります（20文字ルールに従う）

**重要**:
- 4つの項目は必ず黄・赤・緑・青の順
- `margin-bottom: 0` で隙間なく配置
- 角は四角（border-radiusなし）

### 9. 購入CTAセクション

```html
<div class="cta">
    <h2>【運命が動く24時間】</h2>

    <p style="margin-bottom: 30px;">今、あなたの守護神、守護霊は、<br>あなたがこの鑑定を読んだことに<br>気づいています。</p>
    <p style="margin-bottom: 30px; font-size: 1.15em; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">「この人は、守護を求めている」<br>「力を貸してあげたい」<br>「運命を動かす手助けを<br>してあげたい」</p>
    <p style="margin-bottom: 30px;">でも、この流れは長く続きません。</p>
    <p style="margin-bottom: 30px;">何もしなければ、<br>今の延長線上の未来が待っています。</p>
    <p style="margin-bottom: 30px; font-weight: bold;">ただ、今から24時間。<br>この間に決断すれば、<br>運命はスムーズに好転し始めます。</p>
    <p style="margin-bottom: 30px;">「ちゃんと守護を受け取りたい」<br>そう感じた方だけ、進んでください。</p>

    <div class="price">
        <span class="original-price">通常9,800円</span><br>
        <span class="limited-badge">24時間限定の特別価格</span><br>
        <span class="special-price">4,980円</span>
    </div>

    <a href="https://lnuwhrs3tncycy5pf0r3.stores.jp/items/69eb763d23b5d0e88f9854e9" class="cta-button" target="_blank">本式守護鑑定を受ける▼</a>

    <p style="margin-top: 30px;">お申し込み後、<br>購入時のお名前をお知らせください。<br>1日以内に、あなただけの<br>鑑定書をお届けします。</p>
</div>
```

**重要**:
- 守護霊の声は太字・大きめ・白強調
- 「ただ、今から24時間」は太字のみ
- 価格は`.special-price`でゴールド
- 限定バッジは`.limited-badge`で赤
- 20文字ルールに従って改行（細切れにしない）

### 10. クロージングセクション

```html
<div class="closing">
    <p style="margin-bottom: 30px;">私には視えています。</p>
    <p style="margin-bottom: 30px;">あなたのオーラが整い、<br>守護神からのエネルギーを<br>受け取ったとき。</p>
    <p style="margin-bottom: 30px; font-weight: bold;">家族みんなが笑顔で食卓を囲み、<br>温かな会話が弾んでいる場面が。<br>お金の不安から解放され、<br>あなたが穏やかに微笑んでいる姿が。<br>お子さんたちが安心した表情で、<br>あなたに甘えている未来が。</p>
    <p style="margin-bottom: 40px;">その未来へ、私がお連れしますね。</p>

    <div class="signature">深雪</div>
</div>

    </div>
</body>
</html>
```

**重要**:
- ビジョン部分は太字
- ビジョンは20文字ルールに従って改行
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

4. **改行を確認**
   - スマホ表示を基準に改行を調整
   - **20文字ルール**: 1行が20文字を超える場合は改行を入れる
   - **改行位置**: 読点(、)や助詞(は、が、を、に、も、で、と)の直後で改行
   - **できるだけ長く**: 20文字以内なら1行にまとめる（無駄に細切れにしない）
   - 段落間は`<p>`で分ける
   - 段落内は`<br>`で改行

   **改行の処理フロー**:
   1. まず全文を<br>なしで並べる
   2. 20文字を超える箇所を見つける
   3. その直前の読点(、)や助詞の後で改行を入れる

   **例**:
   ```html
   <!-- ❌ ダメ: 無駄に細切れ -->
   <p>力強く、<br>どっしりとした<br>生命力を<br>持っています。</p>

   <!-- ✅ 良い: 20文字を基準に自然な位置で改行 -->
   <p>力強く、どっしりとした<br>生命力を持っています。</p>
   <!-- 「力強く、どっしりとした」(13文字) + 「生命力を持っています。」(12文字) -->
   ```

5. **強調箇所を確認**
   - 本質: 黄色強調
   - オーラを整え〜: 白強調
   - でも、ここで流れを変えたら: 白強調
   - 質問部分: 白強調
   - リスト: 自動的に黄色太字

---

## チェックリスト

作成完了後、以下を確認：

- [ ] フォルダ名が`miyuki/連番_名前様M/`形式になっている
- [ ] HTMLファイル名が`index.html`になっている
- [ ] タイトルに正しい名前が入っている
- [ ] 守護神名が正しく設定されている
- [ ] 画像パスが`../鑑定画像/守護神名.png`になっている
- [ ] oracle-message::beforeが`content: ''`になっている（✨なし）
- [ ] bodyに`font-size: 17px`が設定されている（PC表示）
- [ ] スマホ用メディアクエリで`font-size: 15px`が設定されている
- [ ] ctaのpaddingが`40px 25px`になっている
- [ ] closingのpaddingが`30px 15px`になっている
- [ ] スマホ用メディアクエリでctaのpaddingが`40px 15px`になっている
- [ ] スマホ用メディアクエリでclosingのpaddingが`30px 10px`になっている
- [ ] 「本式守護鑑定でお伝えすること」のfont-sizeが`1.3em`になっている
- [ ] 「⛩️なぜ今、<br>　悪いものを引き寄せているのか」に改行と全角スペースが入っている
- [ ] 4つの項目が黄・赤・緑・青の順で配置されている
- [ ] 4つの項目のmargin-bottomが0になっている（隙間なし）
- [ ] 「守護神から守護を<br>受け取る方法」に改行が入っている
- [ ] 「守護の力を手に入れた<br>あなたの未来」に改行が入っている
- [ ] 「私の守護の力をあなたに」（、なし）になっている
- [ ] STORES URLが`https://lnuwhrs3tncycy5pf0r3.stores.jp/items/69eb763d23b5d0e88f9854e9`になっている
- [ ] 署名が「深雪」になっている（深幸→深雪に変更）
- [ ] 改行が20文字ルールに従っている
- [ ] 強調すべき箇所が正しく強調されている
- [ ] リスト項目が`<ul><li>`で記述されている
- [ ] 本質の部分が黄色強調になっている
- [ ] ビジョン部分が太字になっている

---

## よく使うスタイルパターン集

### 段落（通常）
```html
<p style="margin-bottom: 30px;">テキスト</p>
```

### 段落（強調・白）
```html
<p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">テキスト</p>
```

### 段落（強調・黄色）- 本質部分に使用
```html
<p style="margin-bottom: 30px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">テキスト</p>
```

### 段落（太字のみ）- ビジョン部分に使用
```html
<p style="margin-bottom: 30px; font-weight: bold;">テキスト</p>
```

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

**理由**: 左右の余白を最小限にすることで、スマホでも1行に約20文字表示できるようになり、`<br>`による意図的な改行が正しく機能します。

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

### モバイル対応チェックポイント

新規作成時は以下を確認してください：

**フォントサイズ:**
- [ ] bodyに`font-size: 17px`が設定されている（PC表示）
- [ ] スマホ用メディアクエリでbodyに`font-size: 15px`が設定されている
- [ ] 「本式守護鑑定でお伝えすること」が`font-size: 1.3em`になっている

**横幅・padding:**
- [ ] `.special-price` に `white-space: nowrap` が含まれている
- [ ] ctaのpaddingが`40px 25px`になっている（PC）
- [ ] closingのpaddingが`30px 15px`になっている（PC）
- [ ] **重要**: スマホ用メディアクエリで`body`, `.container`, `.oracle-message`, `.section`の左右paddingが10pxになっている
- [ ] **重要**: スマホ用メディアクエリでctaのpaddingが`40px 15px`になっている
- [ ] **重要**: スマホ用メディアクエリでclosingのpaddingが`30px 10px`になっている

**改行ルール:**
- [ ] **重要**: テキストの改行が20文字ルールに従っている
- [ ] 無駄に細切れになっていない（20文字以内なら1行に）
- [ ] 文節の途中で改行していない

**表示確認:**
- [ ] 実際のスマートフォンまたはブラウザのデベロッパーツールで表示確認済み
- [ ] 価格が1行で表示される
- [ ] 文章の改行が自然で、変な位置で自動改行されていない
- [ ] ボタンが適切なサイズで表示される
- [ ] CTAカードと閉じカードの文字が横幅に収まっている

### テスト方法

1. **Chrome DevTools**
   - F12でデベロッパーツールを開く
   - デバイスツールバー（Ctrl+Shift+M / Cmd+Shift+M）を有効化
   - iPhone SEやiPhone 12 Proなどのプリセットで確認

2. **実機テスト**
   - Cloudflare Pagesにデプロイ後、実際のスマートフォンで確認
   - 特に価格表示と文章の改行を重点的にチェック

---

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

### 改行ルール
1. **20文字ルール**: 1行20文字以内を目安に改行
2. **できるだけ長く**: 20文字以内なら1行にまとめる
3. **改行位置**: 読点(、)、助詞の直後
4. **文節の途中で改行しない**: 絶対禁止

### 特殊な改行
- 「⛩️なぜ今、<br>　悪いものを引き寄せているのか」← 2行目に全角スペース
- 「守護神から守護を<br>受け取る方法」
- 「守護の力を手に入れた<br>あなたの未来」
- 「私の守護の力をあなたに」← 、なし

---

## 改行ルール詳細（スマホ対応）

### 基本方針

スマホで1行に表示できる文字数は**約15-20文字**です。この制限を踏まえて、意図的に改行を入れることで、読みやすい表示を実現します。

### 20文字ルール

1. **まず全文を並べる**: `<br>`なしで文章を書く
2. **20文字を超える箇所を見つける**: 1行が20文字を超えていないか確認
3. **自然な位置で改行**: 読点(、)や助詞の直後で`<br>`を入れる
4. **できるだけ長く**: 20文字以内なら無駄に細切れにせず1行にまとめる

### 改行位置の優先順位

改行は以下の位置で行います：

1. **読点(、)の直後** - 最優先
2. **句点(。)の直後** - 文の区切り
3. **助詞の直後** - は、が、を、に、も、で、と
4. **接続詞の直後** - でも、しかし、そして、など

**絶対にやってはいけないこと**:
- 文節の途中で改行（例: 「家族を」で改行して「包み込む」が次の行）

### 具体例

#### ❌ ダメな例1: 無駄に細切れ

```html
<p>お金のこと、<br>お子さんのこと、<br>精神状態。</p>
```
- 「お金のこと、お子さんのこと、精神状態。」は20文字なので1行でOK

#### ✅ 良い例1: 20文字なら1行に

```html
<p>お金のこと、お子さんのこと、精神状態。<br>全てが重なって、<br>心が押しつぶされそうになっている。</p>
```
- 1行目: 20文字 ← ちょうど20文字
- 2行目: 9文字 ← 短いが、次と繋げると29文字になるので分ける
- 3行目: 19文字 ← 20文字以内

#### ❌ ダメな例2: 文節の途中で改行

```html
<p>力強く、<br>どっしりとした<br>生命力を<br>持っています。</p>
```
- 「どっしりとした」と「生命力を」は一緒にすべき

#### ✅ 良い例2: 自然な区切り

```html
<p>力強く、どっしりとした生命力を<br>持っています。</p>
```
- 1行目: 17文字
- 2行目: 8文字

#### ❌ ダメな例3: 細切れすぎる強調文

```html
<p style="font-weight: bold; color: #f0f0ff;">オーラを整え、<br>守護神からのエネルギーを<br>正しく受け取れば、<br>お金の流れも、<br>お子さんとの関係も、<br>精神状態も、<br>必ず変わります。</p>
```
- それぞれの行が8〜13文字で短すぎる

#### ✅ 良い例3: できるだけ長く

```html
<p style="font-weight: bold; color: #f0f0ff;">オーラを整え、守護神からのエネルギーを<br>正しく受け取れば、お金の流れも、<br>お子さんとの関係も、精神状態も、<br>必ず変わります。</p>
```
- 1行目: 19文字
- 2行目: 18文字
- 3行目: 18文字
- 4行目: 8文字

#### ✅ 良い例4: 見出しの改行

```html
<h2 class="emoji-header">⛩️なぜ今、<br>　悪いものを引き寄せているのか</h2>
```
- 長い見出しは改行して、2行目に全角スペースでインデント

### AIに修正させる場合の指示

AIに改行を修正させる場合は、以下のように指示してください：

```
1行を20文字以内に抑えること。
改行位置は必ず以下のいずれかにすること:
- 読点(、)の直後
- 句点(。)の直後
- 助詞(は、が、を、に、も、で、と)の直後
- 接続詞の直後

絶対に文節の途中で改行しないこと。
20文字以内なら1行にまとめること。
```

### 処理フロー（プログラム的に考える場合）

#### 手動で修正する場合

1. **テキストをまず長く繋げる**
   - 既存の`<br>`を全て削除
   - 読点(、)や句点(。)で繋げて、できるだけ長い文章にする

2. **文字数をカウント**
   - 1行が20文字を超えているか確認
   - 20文字以内なら次の文へ

3. **20文字を超える場合、改行位置を探す**
   - 優先順位1: 最後の読点(、)の直後
   - 優先順位2: 最後の助詞(は、が、を、に、も、で、と)の直後
   - 優先順位3: 接続詞の直後
   - その位置に`<br>`を挿入

4. **改行後、残りの文も同じようにチェック**
   - 2行目以降も同様に20文字ルールを適用

#### AIに指示する場合

```
以下のHTMLファイルの改行を修正してください。

ルール:
1. 1行を20文字以内に抑えること
2. 改行位置は必ず以下のいずれかにすること:
   - 読点(、)の直後
   - 句点(。)の直後
   - 助詞(は、が、を、に、も、で、と)の直後
   - 接続詞の直後
3. 絶対に文節の途中で改行しないこと
4. 20文字以内なら1行にまとめること（無駄に細切れにしない）
```

#### 実例: 修正前 → 修正後

**修正前（細切れ）:**
```html
<p>これまで、<br>あなたは家族のために<br>懸命に頑張ってきた。<br>母として、<br>妻として、<br>しっかりと<br>守ろうとしてきた。</p>
```

**修正後（20文字ルール適用）:**
```html
<p>これまで、あなたは家族のために<br>懸命に頑張ってきた。<br>母として、妻として、<br>しっかりと守ろうとしてきた。</p>
```

各行の文字数:
- 1行目: 17文字
- 2行目: 13文字
- 3行目: 11文字
- 4行目: 17文字
