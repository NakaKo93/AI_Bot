document.addEventListener('DOMContentLoaded', function() {
    var chatForm = document.getElementById('chat-form');

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault(); 

        // form内のデータをobjectに変換
        const formData = new FormData(chatForm);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // URLを取得
        const actionUrl = new URL(chatForm.action);

        // 非同期処理
        fetch(actionUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                console.error('チャットの送信に失敗しました', error);
            }
            return response.json();
        })
        .then(data => {
            // HTMLのメッセージ部分を編集
            const chatContainer = document.getElementById('chat-box');
            // 既存のHTMLのメッセージを消去
            chatContainer.innerHTML = '';

            // HTMLのメッセージを追加
            data.all_chat_history.forEach(chat => {
                const messageElement = document.createElement('li');
                messageElement.classList.add();
                messageElement.innerHTML = `${chat}`;
                chatContainer.appendChild(messageElement);
            });
            
            // テキストエリアの中身を消去する
            document.getElementById('user-input').value = '';
        })
        .catch(error => {
            console.error('チャットの送信に失敗しました', error);
        });
    });
});