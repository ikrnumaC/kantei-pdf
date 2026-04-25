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
    padding: 40px;
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
    padding: 30px;
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
    .container {
        padding: 20px;
    }

    h1 {
        font-size: 1.5em;
    }

    h2 {
        font-size: 1.2em;
    }

    .oracle-message,
    .section {
        padding: 15px;
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
    <p style="margin-bottom: 30px;">【名前】様、</p>
    <p style="margin-bottom: 30px;">視えました。</p>
    <p class="guardian" style="margin-bottom: 30px;">あなたを守っているのは、<br>【守護神名】。</p>
    <p>【守護神の説明】</p>
    <img src="../鑑定画像/【守護神名】.png" alt="【守護神名】" class="guardian-image">
</div>
```

**重要**:
- 画像は相対パス `../鑑定画像/守護神名.png` で参照
- 画像ファイル名は守護神名と完全一致させる

### 3. オーラ・本質セクション

```html
<div class="section">
    <p style="margin-bottom: 30px;">あなたのオーラは、<br>【オーラの色・説明】。<br>【特徴】。</p>
    <p style="margin-bottom: 30px;">【守護神名】に守られる人は、<br>【特徴1】、<br>【特徴2】。</p>
    <p style="margin-bottom: 30px; color: #ffd966; font-weight: bold; text-shadow: 0 0 15px rgba(255, 217, 102, 0.4);">【本質の説明】<br>それがあなたの本質です。</p>
    <p style="margin-bottom: 30px;">これほど強い守護神に守られているのに、<br>今、流れが悪くなっている…</p>
    <p>その原因をお伝えします。</p>
</div>
```

**重要**: 本質の部分は必ず黄色強調にする

### 4. お悩みセクション

```html
<h2 class="emoji-header">⛩️お悩みについて</h2>
<div class="section">
    <p style="margin-bottom: 30px;">【お悩みの内容】</p>
    <p style="margin-bottom: 30px;">【現状の説明】</p>
    <p style="margin-bottom: 30px;">この問題は、<br>実はあなたが悪いわけではありません。</p>
    <p style="font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">オーラを整え、<br>守護神からのエネルギーを正しく受け取れば、<br>【変化する内容】、必ず変わります。</p>
</div>
```

**重要**: 最後の段落は必ず白強調にする

### 5. なぜ今、悪いものを引き寄せているのか

```html
<h2 class="emoji-header">⛩️なぜ今、悪いものを引き寄せているのか</h2>
<div class="section">
    <p style="margin-bottom: 20px;">【時期の説明】<br>こんなことがありませんでしたか?</p>
    <ul style="margin-bottom: 30px;">
        <li>【項目1】</li>
        <li>【項目2】</li>
        <li>【項目3】</li>
    </ul>
    <p style="margin-bottom: 30px;">それらは、守護神の力が弱まり、<br>あなたを守るオーラが少なくなってしまったことで起こっているのです。</p>
    <p style="margin-bottom: 30px;">【本来の力の説明】</p>
    <p style="margin-bottom: 30px;">【これまでの頑張りの説明】</p>
    <p style="margin-bottom: 30px;">でも今、守護の力が弱くなってきている…</p>
    <p>だから、【失われたもの1】、<br>【失われたもの2】、<br>今は失われてしまっているのです。</p>
</div>
```

**重要**: リストは自動的に黄色太字になる

### 6. 二つの道

```html
<h2 class="emoji-header">⛩️二つの道</h2>
<div class="section">
    <p style="margin-bottom: 30px;">このまま、オーラが乱れたままだと、<br>【悪い未来1】<br>【悪い未来2】</p>
    <p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">でも、ここで流れを変えたら。</p>
    <p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">オーラが整い、守護の力を受け取れるようになり、<br>【良い未来1】<br>【良い未来2】</p>
    <p>どちらの道を歩むかは、<br>まだ今なら、あなた自身で選べます。</p>
</div>
```

**重要**: 「でも、ここで流れを変えたら。」と良い未来の部分は白強調にする

### 7. 守護の方法

```html
<h2 class="emoji-header">⛩️守護の方法</h2>
<div class="section">
    <p style="margin-bottom: 30px;">ここまでの鑑定で、<br>あなたの守護神とオーラの状態と、<br>なぜ今のような状況なのかをお伝えしました。</p>
    <p style="margin-bottom: 30px;">でも、一番大事なのはここから、</p>
    <p style="margin-bottom: 30px; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">「じゃあ、具体的にどうすれば良くなるのか」<br>「理想の未来を手に入れるためには、何をすればいいのか」<br>ということですよね。</p>
    <p style="margin-bottom: 30px;"><span style="font-size: 1.4em; font-weight: bold; color: #c8d0ff;">【本式守護鑑定】</span>では、<br>あなたが実際に守護を受け取るための<br>"具体的な方法"</p>
    <p>そして、<br>未来が明るく広がるタイミングを<br>お伝えいたします。</p>
</div>
```

**重要**: 質問部分は白強調、【本式守護鑑定】は大きく強調

### 8. 本式守護鑑定でお伝えすること（4色ボックス）

```html
<div style="padding: 40px 0; margin: 40px 0;">
    <h2 style="text-align: center; color: #c8d0ff; font-size: 1.5em; margin-bottom: 50px; border: none; text-shadow: 0 0 20px rgba(168, 184, 255, 0.5);">🔮 本式守護鑑定でお伝えすること</h2>

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
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ 守護神から守護を受け取る方法</h3>
                <p>【説明文 - テキストから抽出】</p>
            </div>
        </div>

        <!-- 項目3: 緑背景 -->
        <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(52, 199, 89, 0.7); opacity: 0.3;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ 守護の力を手に入れたあなたの未来</h3>
                <p>【説明文 - テキストから抽出】</p>
            </div>
        </div>

        <!-- 項目4: 青背景 -->
        <div style="position: relative; padding: 40px 30px; margin-bottom: 0;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 122, 255, 0.7); opacity: 0.3;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="font-size: 1.4em; font-weight: bold; color: #c8d0ff; margin-bottom: 15px;">⛩️ 私の守護の力を、あなたに</h3>
                <p>【説明文 - テキストから抽出】</p>
            </div>
        </div>
    </div>

    <p style="margin-top: 30px; text-align: center;">このまま方法を知らずに過ごすか、<br>守護を受け取る道を選ぶか。<br>決めるのは、あなたです。</p>
</div>
```

**重要**:
- 4つの項目は必ず黄・赤・緑・青の順
- `margin-bottom: 0` で隙間なく配置
- 角は四角（border-radiusなし）

### 9. 購入CTAセクション

```html
<div class="cta">
    <h2>【運命が動く24時間】</h2>

    <p style="margin-bottom: 30px;">今、あなたの守護神、守護霊は、<br>あなたがこの鑑定を読んだことに気づいています。</p>
    <p style="margin-bottom: 30px; font-size: 1.15em; font-weight: bold; color: #f0f0ff; text-shadow: 0 0 10px rgba(200, 200, 255, 0.3);">「この人は、守護を求めている」<br>「力を貸してあげたい」<br>「運命を動かす手助けをしてあげたい」</p>
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

    <p style="margin-top: 30px;">お申し込み後、<br>購入時のお名前をお知らせください。<br>1日以内に、あなただけの鑑定書をお届けします。</p>
</div>
```

**重要**:
- 守護霊の声は太字・大きめ・白強調
- 「ただ、今から24時間」は太字のみ
- 価格は`.special-price`でゴールド
- 限定バッジは`.limited-badge`で赤

### 10. クロージングセクション

```html
<div class="closing">
    <p style="margin-bottom: 30px;">私には視えています。</p>
    <p style="margin-bottom: 30px;">あなたのオーラが整い、<br>守護神からのエネルギーを受け取ったとき。</p>
    <p style="margin-bottom: 30px; font-weight: bold;">【ビジョン1】<br>【ビジョン2】<br>【ビジョン3】</p>
    <p style="margin-bottom: 40px;">その未来へ、私がお連れしますね。</p>

    <div class="signature">深雪</div>
</div>

    </div>
</body>
</html>
```

**重要**:
- ビジョン部分は太字
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
   - 元のテキストの改行位置を守る
   - 段落間は`<p>`で分ける
   - 段落内は`<br>`で改行

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
- [ ] 4つの項目が黄・赤・緑・青の順で配置されている
- [ ] 4つの項目のmargin-bottomが0になっている（隙間なし）
- [ ] STORES URLが`https://lnuwhrs3tncycy5pf0r3.stores.jp/items/69eb763d23b5d0e88f9854e9`になっている
- [ ] 署名が「深雪」になっている（深幸→深雪に変更）
- [ ] 改行が元のテキストと一致している
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
