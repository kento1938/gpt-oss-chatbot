# LM Studio Chat Web App

LM Studio と連携した ChatGPT 風の Web チャットアプリケーション

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)
![LM Studio](https://img.shields.io/badge/LM%20Studio-1.4.1-orange.svg)

## 📝 概要

コマンドライン版の LM Studio チャットボットを、モダンな Web アプリケーションに進化させました。ChatGPT のような直感的な UI で、LM Studio でホストされているローカル AI モデルとチャットできます。

## ✨ 主な機能

- 🎨 **ChatGPT 風 UI**: ダークテーマのモダンなデザイン
- 💬 **リアルタイムチャット**: Web ベースで AI と対話
- 🔄 **セッション管理**: 会話履歴の保持とクリア機能
- 🛡️ **エラーハンドリング**: LM Studio 未接続時のフォールバック
- 📱 **レスポンシブデザイン**: PC・モバイル対応
- ⚡ **自動応答処理**: LM Studio の特殊タグを自動除去

## 🏗️ 技術スタック

### バックエンド

- **Flask**: Web フレームワーク
- **Flask-CORS**: クロスオリジン対応
- **lmstudio**: LM Studio 連携ライブラリ

### フロントエンド

- **HTML5/CSS3**: ChatGPT 風 UI
- **JavaScript**: リアルタイム通信
- **レスポンシブデザイン**: モバイル対応

## 📁 プロジェクト構成

```
LLMOSS/
├── app.py                   # Flaskメインアプリ
├── script.py               # 元のコマンドライン版
├── test.py                 # テストファイル
├── requirements.txt        # 依存関係
├── README.md              # このファイル
├── venv/                  # Python仮想環境
├── templates/
│   └── index.html         # メインページ
└── static/
    ├── style.css          # スタイルシート
    └── script.js          # フロントエンドJS
```

## 🚀 セットアップ手順

### 1. 前提条件

- Python 3.11 以上
- LM Studio（モデルがロード済み）
- Git

### 2. プロジェクトのクローン

```bash
git clone <your-repository-url>
cd LLMOSS
```

### 3. 仮想環境の作成とアクティベート

```bash
# 仮想環境作成（既に作成済みの場合はスキップ）
python -m venv venv

# 仮想環境のアクティベート
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 5. LM Studio の設定

1. LM Studio アプリケーションを起動
2. 使用したいモデルをダウンロード・ロード
3. ローカルサーバーを開始
4. `app.py`内のモデル名を確認・調整

```python
model = lms.llm("openai/gpt-oss-20b")  # 使用するモデル名
```

### 6. アプリケーションの起動

```bash
python app.py
```

### 7. ブラウザでアクセス

- ローカル: http://127.0.0.1:5000

## 🎯 使用方法

1. **チャット開始**: ブラウザでアプリにアクセス
2. **メッセージ送信**:
   - 入力欄にメッセージを入力
   - Enter キーまたは送信ボタンをクリック
   - Shift+Enter で改行
3. **履歴管理**: 「会話をクリア」ボタンで履歴リセット
4. **セッション**: ブラウザを閉じるまで会話履歴を保持

## 🔧 設定とカスタマイズ

### モデルの変更

`app.py`の以下の部分を編集：

```python
model = lms.llm("your-model-name")
```

### ポート変更

`app.py`の最後の部分を編集：

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # ポート番号を変更
```

### UI テーマのカスタマイズ

`static/style.css`を編集してカラーテーマや外観を変更できます。

## 📡 API 仕様

### チャット送信

```http
POST /api/chat
Content-Type: application/json

{
  "message": "こんにちは",
  "session_id": "optional-session-id"
}
```

### レスポンス

```json
{
  "response": "こんにちは！どのようなことについてお聞きになりたいですか？",
  "session_id": "generated-session-id"
}
```

### その他のエンドポイント

- `GET /`: メインページの表示
- `GET /api/history/<session_id>`: 会話履歴の取得
- `POST /api/clear/<session_id>`: 会話履歴のクリア

## 🔍 トラブルシューティング

### LM Studio 接続エラー

**症状**: "LM Studio との接続に問題があります"

**解決方法**:

1. LM Studio が起動していることを確認
2. モデルが正しくロードされていることを確認
3. `app.py`のモデル名が正しいことを確認

### 仮想環境エラー

**症状**: モジュールが見つからない

**解決方法**:

```bash
# 仮想環境が有効になっていることを確認
which python  # Linux/macOS
where python  # Windows

# 依存関係を再インストール
pip install -r requirements.txt
```

## 🎨 UI 特徴

- **ダークテーマ**: 目に優しい暗い配色
- **タイピングインジケーター**: AI 応答中のアニメーション
- **メッセージ区別**: ユーザーと AI メッセージの視覚的区別
- **自動スクロール**: 新しいメッセージまで自動スクロール
- **レスポンシブ**: 様々な画面サイズに対応
