class ChatApp {
    constructor() {
        this.sessionId = null;
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.chatMessages = document.getElementById('chatMessages');
        
        this.initEventListeners();
        this.autoResizeTextarea();
    }

    initEventListeners() {
        // 送信ボタンのクリックイベント
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enterキーでメッセージ送信（Shift+Enterで改行）
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // クリアボタンのクリックイベント
        this.clearBtn.addEventListener('click', () => this.clearChat());

        // テキストエリアの自動リサイズ
        this.messageInput.addEventListener('input', () => this.autoResizeTextarea());
    }

    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 200) + 'px';
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // UI更新
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.autoResizeTextarea();
        this.toggleSendButton(false);
        
        // タイピングインジケーターを表示
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                // セッションIDを保存
                this.sessionId = data.session_id;
                
                // タイピングインジケーターを削除
                this.hideTypingIndicator();
                
                // ボットの返答を表示
                this.addMessage(data.response, 'assistant');
            } else {
                this.hideTypingIndicator();
                this.addMessage(`エラー: ${data.error}`, 'error');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage(`通信エラー: ${error.message}`, 'error');
        } finally {
            this.toggleSendButton(true);
        }
    }

    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;
        
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        
        // 最新メッセージまでスクロール
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant-message typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        typingDiv.innerHTML = `
            <div class="message-content">
                <span>入力中</span>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    toggleSendButton(enabled) {
        this.sendBtn.disabled = !enabled;
    }

    async clearChat() {
        if (!confirm('会話履歴をクリアしますか？')) {
            return;
        }

        try {
            if (this.sessionId) {
                await fetch(`/api/clear/${this.sessionId}`, {
                    method: 'POST'
                });
            }
            
            // UI上のメッセージをクリア（初期メッセージ以外）
            const messages = this.chatMessages.querySelectorAll('.message');
            messages.forEach((message, index) => {
                if (index > 0) { // 最初のメッセージ（挨拶）は残す
                    message.remove();
                }
            });
            
            // セッションIDをリセット
            this.sessionId = null;
            
        } catch (error) {
            console.error('チャットのクリアに失敗しました:', error);
            alert('チャットのクリアに失敗しました。');
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// アプリケーション開始
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
