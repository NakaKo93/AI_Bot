import os
from openai import OpenAI, OpenAIError

class ChatService:
  def __init__(self, getMyLogger):
      # loggerの設定
      self.logger = getMyLogger(__name__)
  
  def load_api_key(self):
    """
    APIキーを読み込む関数
    :return         : 処理の成否
    """
    file_path = os.path.join(os.path.dirname(__file__), 'key.txt')

    try:
      with open(file_path, 'r') as file:
        key = file.read().strip()
      self.logger.info("APIキーの読み込みに成功しました")
      return key
    except Exception as e:
      self.logger.error(f"APIキーの読み込みに失敗しました: {e}")
      return False

  def reboot_chat(self):
    """
    チャット再起動用の関数
    """

  def get_chatbot_response(self, key, chat_history, prompt):
    """
    チャット返答用の関数
    :param  key         : APIキー
    :param  chat_history: チャットの履歴
    :param  prompt      : ユーザーの質問内容
    :return       : 返答内容
    :return       : チャットを終了 or 続ける
    """
    # 固定のメッセージ
    system_message = {"role": "system", "content": "あなたは37才で、コードレビュアーの佐藤です。副業で忍者をしているので「ござる」という語尾でしゃべります。"}

    # 追加する固定の回答履歴
    fixed_history = [
        {"role": "user", "content": "あなたは誰ですか？"},
        {"role": "assistant", "content": "私はコードレビュアーの佐藤でござる。副業で忍者をしているでござるよ。"}
    ]

    # ユーザーからの質問内容
    user_message = [
      {"role": "user", "content": prompt}
    ]

    # 呼び出す関数の設定
    functions = [
      {
        "name": "reboot_chat",
        "description": "チャットの再起動を行う関数",
        "parameters": {
          "type": "object",
          "properties": {},
        },
      },
    ]

    # chatGPT
    client = OpenAI(api_key = key)

    try:
      response = client.chat.completions.create(
        # 使用するChatGPTのモデル
        model = "gpt-4o",
        messages = system_message + fixed_history + chat_history + user_message,
        functions = functions,
        # 出力するトークン(文字)上限
        max_tokens = 150
      )

      response_text = response.choices[0].message
      function_call = getattr(response.choices[0], "function_call", None)

      # 呼び出された関数の処理
      if function_call:
        if function_call["name"] == "reboot_chat":
          should_reboot = True
      else:
        should_reboot = False

      return response_text, should_reboot
    except OpenAIError as e:
      self.logger.error(f"APIリクエストに失敗しました: {e}")

      response_text = "APIリクエストに失敗しました。"
      should_reboot = False

      return response_text, should_reboot