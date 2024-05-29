from flask import  session
from chatGPT.chat import load_key, change_key, get_chatbot_response


class ChatAction:
    def change_key(self, input_key):
        """
        APIキーの変更
        """
        status = change_key(input_key)
        if status:
            message = "キーの変更に成功しました"

            return message
        else:
            message = "キーの変更に失敗しました"

            return message

    def first_action(self):
        """
        初回起動
        """
        # 履歴の初期化
        chat_history = []
        all_chat_history = []

        # APIキーの読み込み
        key = load_key()
        if not key:
            all_chat_history.append("APIキーの読み込み、認証に失敗しました。リダイレクトしてください。")

            return chat_history, all_chat_history
        else:
            # 正常に読み込まれた場合の処理
            all_chat_history.append("起動しました。'reboot'または、再起動を表すメッセージの入力で再起動します。")
            # レスポンスの受け取り
            user_input = "はじめまして"
            response_text, _ = get_chatbot_response(key, chat_history, user_input)
            # 履歴の保存
            all_chat_history.append("bot :")
            all_chat_history.append(f"{response_text}")
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": response_text})

            return chat_history, all_chat_history


    def action(self, user_input, chat_history, all_chat_history):
        """
        二回目以降の起動
        """
        # APIキーの読み込み
        key = load_key()
        if not key:
            all_chat_history.append("APIキーの読み込みに失敗しました。リダイレクトしてください。")
            return all_chat_history

        # 履歴の保存
        all_chat_history.append("you :")
        all_chat_history.append(f"{user_input}")

        # レスポンスの受け取り
        response_text, should_reboot = get_chatbot_response(key, chat_history, user_input)

        # 再起動する場合
        if (user_input.lower() in ['reboot']) or (should_reboot):
            reboot_status = True

            return chat_history, all_chat_history, reboot_status
        
        reboot_status = False

        # 履歴の保存
        all_chat_history.append("bot :")
        all_chat_history.append(f"{response_text}")
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response_text})

        return chat_history, all_chat_history, reboot_status
    

    def reboot_action(self, chat_history, all_chat_history):
        """
        再起動
        """
        # 履歴の初期化
        all_chat_history.append("チャットボットを再起動しました")

        # APIキーの読み込み
        key = load_key()
        if not key:
            all_chat_history.append("APIキーの読み込みに失敗しました。リダイレクトしてください。")

            return all_chat_history
        else:
            # 正常に読み込まれた場合の処理
            all_chat_history.append("起動しました。終了を表すメッセージまたは、'reboot'の入力で再起動します。")
            # レスポンスの受け取り
            user_input = "はじめまして"
            response_text, _ = get_chatbot_response(key, chat_history, user_input)
            # 履歴の保存
            all_chat_history.append("bot :")
            all_chat_history.append(f"{response_text}")
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": response_text})

            return chat_history, all_chat_history