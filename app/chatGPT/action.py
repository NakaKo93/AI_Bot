from log.log_setting import getMyLogger
from chat import load_api_key, get_chatbot_response
from tkinter import *

class ChatBot:
    def __init__(self):
        # loggerの設定
        self.logger = getMyLogger(__name__)
        # 会話履歴を保持するリスト
        self.chat_history = []
        # 全体のメッセージのリスト
        self.all_chat_history = []

    def first_action(self):
        """
        初回起動
        """
        # 履歴があるときの処理
        if self.all_chat_history:
            # 履歴の初期化
            self.chat_history = []
            self.all_chat_history = []
            # 履歴の保存
            self.logger.info("チャットボットを再起動")
            self.all_chat_history.append("チャットボットを再起動しました")

        # APIキーの読み込み
        key = load_api_key()
        if not key:
            self.all_chat_history.append("APIキーの読み込みに失敗しました。リダイレクトしてください。")

            return self.all_chat_history
        else:
            # 正常に読み込まれた場合の処理
            self.all_chat_history.append("起動しました。終了を表すメッセージまたは、'reboot'の入力で再起動します。")
            # レスポンスの受け取り
            user_input = "はじめまして"
            response_text, _ = get_chatbot_response(key, self.chat_history, user_input)
            # 履歴の保存
            self.all_chat_history.append(f"bot : {response_text}")
            self.chat_history.append({"role": "user", "content": user_input})
            self.chat_history.append({"role": "assistant", "content": response_text})

            return self.all_chat_history


    def action(self, chat):
        """
        二回目以降の起動
        """
        # APIキーの読み込み
        key = load_api_key()
        if not key:
            self.all_chat_history.append("APIキーの読み込みに失敗しました。リダイレクトしてください。")
            return self.all_chat_history

        # チャットの処理
        user_input = chat
        # 履歴の保存
        self.all_chat_history.append(f"you : {user_input}")
        # レスポンスの受け取り
        response_text, should_reboot = get_chatbot_response(key, self.chat_history, user_input)

        # 終了する場合
        if (user_input.lower() in ['reboot']) or (should_reboot):
            # 初回起動用の関数
            self.firstaction()

            return self.all_chat_history
        
        # 履歴の保存
        self.all_chat_history.append(f"bot : {response_text}")
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append({"role": "assistant", "content": response_text})

        return self.all_chat_history