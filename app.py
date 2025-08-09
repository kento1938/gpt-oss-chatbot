from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

# LM Studio設定
LM_STUDIO_AVAILABLE = True
model = None

try:
    import lmstudio as lms
    # LM Studioでホストされているモデルを指定します
    model = lms.llm("openai/gpt-oss-20b")
    print("LM Studio接続成功")
except Exception as e:
    print(f"LM Studio接続失敗: {e}")
    print("ダミーモードで動作します")
    LM_STUDIO_AVAILABLE = False

def extract_message_content(response_text):
    """LM Studioの応答から実際のメッセージ内容を抽出"""
    if not response_text:
        return ""
    
    # <|channel|>final<|message|> の後の内容を抽出
    if "<|channel|>final<|message|>" in response_text:
        parts = response_text.split("<|channel|>final<|message|>")
        if len(parts) > 1:
            return parts[-1].strip()
    
    # 一般的な <|message|> タグの後の内容を抽出
    if "<|message|>" in response_text:
        parts = response_text.split("<|message|>")
        if len(parts) > 1:
            return parts[-1].strip()
    
    # タグが見つからない場合は元のテキストを返す
    return response_text.strip()

# セッション管理のための辞書（本番環境では適切なセッション管理を使用してください）
sessions = {}

@app.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """チャットAPIエンドポイント"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', None)
        
        if not user_message:
            return jsonify({'error': 'メッセージが空です'}), 400
        
        # セッションIDが提供されていない場合は新しいセッションを作成
        if not session_id:
            session_id = str(uuid.uuid4())
            sessions[session_id] = []
        
        # セッションが存在しない場合は新しく作成
        if session_id not in sessions:
            sessions[session_id] = []
        
        # 会話履歴にユーザーメッセージを追加
        sessions[session_id].append({"role": "user", "content": user_message})
        
        # モデルにリクエストを送信
        if LM_STUDIO_AVAILABLE and model:
            try:
                response_obj = model.respond({"messages": sessions[session_id]})
                # レスポンスオブジェクトから文字列を抽出
                if hasattr(response_obj, 'text'):
                    response = response_obj.text
                elif hasattr(response_obj, 'content'):
                    response = response_obj.content
                elif hasattr(response_obj, 'message'):
                    response = response_obj.message
                else:
                    # 属性が分からない場合は文字列変換を試行
                    response = str(response_obj)
                
                print(f"LM Studio レスポンス: {response}")
                
                # レスポンスから実際のメッセージ内容を抽出
                response = extract_message_content(response)
                print(f"抽出されたメッセージ: {response}")
                
            except Exception as lm_error:
                print(f"LM Studio エラー: {lm_error}")
                response = f"申し訳ございません。LM Studioとの接続に問題があります。（エラー: {str(lm_error)}）"
        else:
            # ダミーレスポンス（LM Studioが利用できない場合）
            response = f"こんにちは！あなたのメッセージ「{user_message}」を受け取りました。現在はテストモードで動作しています。LM Studioを起動してモデルを読み込んでください。"
        
        # レスポンスを会話履歴に追加
        sessions[session_id].append({"role": "assistant", "content": response})
        
        # 確実に文字列型にする
        response_str = str(response) if response else "応答を取得できませんでした。"
        
        print(f"最終レスポンス: {response_str}")
        print(f"レスポンスの型: {type(response_str)}")
        
        return jsonify({
            'response': response_str,
            'session_id': session_id
        })
        
    except Exception as e:
        # エラーが発生した場合は、最後のユーザー入力を履歴から削除
        if session_id and session_id in sessions and sessions[session_id]:
            sessions[session_id].pop()
        
        print(f"エラーの詳細: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500

@app.route('/api/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """セッションの会話履歴を取得"""
    if session_id in sessions:
        return jsonify({'history': sessions[session_id]})
    else:
        return jsonify({'history': []})

@app.route('/api/clear/<session_id>', methods=['POST'])
def clear_history(session_id):
    """セッションの会話履歴をクリア"""
    if session_id in sessions:
        sessions[session_id] = []
    return jsonify({'message': '履歴がクリアされました'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
