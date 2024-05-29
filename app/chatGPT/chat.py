import os
from openai import OpenAI, OpenAIError
from log.log_setting import getMyLogger


# loggerの設定
logger = getMyLogger(__name__)


def load_key():
  """
  APIキーを読み込む関数
  :return         : 処理の成否
  """
  # ファイルのパスを指定
  file_path = os.path.join(os.path.dirname(__file__), 'key.txt')

  try:
    with open(file_path, 'r') as file:
      key = file.read().strip()
      logger.info("APIキーの読み込みに成功しました")

      # chatGPT
      client = OpenAI(api_key = key)
      try:
        response = client.chat.completions.create(
          model = "gpt-4o",
          messages = [{"role": "user", "content": 'test'}],
          max_tokens = 1
        )

        return key
      except OpenAIError as e:
        logger.error(f"APIリクエストに失敗しました: {e}")

        return False
  except Exception as e:
    logger.error(f"APIキーの読み込みに失敗しました: {e}")

    return False
  
def change_key(input_key):
  """
  APIキーを変更する関数
  :return         : 処理の成否
  """
  # ファイルのパスを指定
  file_path = os.path.join(os.path.dirname(__file__), 'key.txt')

  # ファイルに上書き、ファイルがなければ作成
  with open(file_path, 'w') as file:
      file.write(input_key)

  try:
    with open(file_path, 'r') as file:
      key = file.read().strip()
      if input_key == key:
        logger.info("APIキーの更新に成功しました")

        return True
      else:
        logger.info("APIキーの更新に失敗しました")

        return False
  except Exception as e:
    logger.error(f"APIキーの生成に失敗しました: {e}")
    
    return False


def reboot_chat():
  """
  チャット再起動用の関数
  """


def get_chatbot_response(key, chat_history, prompt):
  """
  チャット返答用の関数
  :param  key         : APIキー
  :param  chat_history: チャットの履歴
  :param  prompt      : ユーザーの質問内容
  :return       : 返答内容
  :return       : チャットを終了 or 続ける
  """

  # 固定のメッセージ
  system_message = [
    {"role": "system", "content": "あなたは37才で、コードレビュアーの佐藤です。副業で忍者をしているので「ござる」という語尾でしゃべります。改行するときは<br>を文末に付けてください"}
  ]

  # 追加する固定の回答履歴
  fixed_history = [
      {"role": "user", "content": "あなたは誰ですか？"},
      {"role": "assistant", "content": "私はコードレビュアーの佐藤でござる。<br>副業で忍者をしているでござるよ。<br>"}
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

    response_text = response.choices[0].message.content
    function_call = response.choices[0].message.function_call

    logger.info(f"チャット: {response.choices[0].message}")

    # 呼び出された関数の処理
    if function_call:
      if function_call.name == "reboot_chat":
        logger.info("チャットボットを再起動")
        should_reboot = True
    else:
      should_reboot = False

    return response_text, should_reboot
  except OpenAIError as e:
    logger.error(f"APIリクエストに失敗しました: {e}")
    response_text = "APIリクエストに失敗しました。"
    should_reboot = False

    return response_text, should_reboot