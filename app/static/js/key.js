document.addEventListener('DOMContentLoaded', function() {
    var keytForm = document.getElementById('key-form');

    keytForm.addEventListener('submit', function(event) {
        event.preventDefault(); 

        // form内のデータをobjectに変換
        const formData = new FormData(keytForm);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // URLを取得
        const actionUrl = new URL(keytForm.action);

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
                console.error('キーの送信に失敗しました', error);
            }
            return response.json();
        })
        .then(data => {
            // キー表示部分を編集
            const keyContainer = document.getElementById('key-box');
            // 内容のを消去
            keyContainer.innerHTML = '';
            // メッセージを追加
            const messageElement = document.createElement('p');
            messageElement.classList.add();
            messageElement.innerHTML = `${data.message}`;
            keyContainer.appendChild(messageElement);

            // メッセージ部分を編集
            const chatContainer = document.getElementById('chat-box');
            // 内容のを消去
            chatContainer.innerHTML = '';
            // メッセージを追加
            data.all_chat_history.forEach(chat => {
                const messageElement = document.createElement('li');
                messageElement.classList.add();
                messageElement.innerHTML = `${chat}`;
                chatContainer.appendChild(messageElement);
            });

            // テキストエリアの中身を消去する
            document.getElementById('key-input').value = '';
        })
        .catch(error => {
            console.error('キーの送信に失敗しました', error);
        });
    });
});