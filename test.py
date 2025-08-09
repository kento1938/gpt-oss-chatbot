import lmstudio as lms

# LM Studioでホストされているモデルを指定します
model = lms.llm("openai/gpt-oss-20b")

# 会話履歴を保存するためのリスト
messages = []

def chat_bot():
    print("チャットを開始します。会話を終了するには 'exit' と入力してください。")
    while True:
        user_input = input("あなた: ")
        if user_input.lower() == "exit":
            print("チャットを終了します。")
            break

        # 会話履歴にユーザーの入力を追加します
        messages.append({"role": "user", "content": user_input})
        
        try:
            # プロンプトを辞書形式で渡します
            response = model.respond({"messages": messages})
            
            print(f"ボット: {response}")

            # 応答を会話履歴に追加します
            messages.append({"role": "assistant", "content": response})

        except Exception as e:
            print(f"エラーが発生しました: {e}")
            # エラーが発生した場合は、最後のユーザー入力を履歴から削除します
            messages.pop()

# アプリケーションの開始
if __name__ == "__main__":
    chat_bot()