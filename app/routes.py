from flask import request, jsonify, render_template, session
import os
from app import app
import chatGPT

# sessionに用いる暗号化キーの生成
app.secret_key = os.urandom(24)

# インスタンスの作成
chatAction_instance = chatGPT.action.ChatAction()

@app.route('/')
def index():
    # 会話履歴のリスト
    chat_history = []
    # 全体のメッセージのリスト
    all_chat_history = []

    chat_history, all_chat_history = chatAction_instance.first_action()

    # セッションに会話履歴を保存
    session['chat_history'] = chat_history
    session['all_chat_history'] = all_chat_history

    return render_template('index.html', all_chat_history=all_chat_history)


@app.route('/chat-process', methods=['POST'])
def chat_process():
    # ユーザーの質問を取得
    user_input = request.get_json()
    user_input = user_input["user-input"]
    # セッションから会話履歴を取得
    chat_history = session.get('chat_history', [])
    all_chat_history = session.get('all_chat_history', [])

    chat_history, all_chat_history, reboot_status = chatAction_instance.action(user_input, chat_history, all_chat_history)
    if reboot_status:
        chat_history, all_chat_history = chatAction_instance.reboot_action(chat_history, all_chat_history)

    # セッションに会話履歴を保存
    session['chat_history'] = chat_history
    session['all_chat_history'] = all_chat_history
    
    return jsonify({"all_chat_history": all_chat_history})


@app.route('/change-key', methods=['POST'])
def change_key():
    # キーを取得
    input_key = request.get_json()
    input_key = input_key['key-input']
    message = chatAction_instance.change_key(input_key)

    # 会話履歴のリスト
    chat_history = []
    # 全体のメッセージのリスト
    all_chat_history = []

    chat_history, all_chat_history = chatAction_instance.first_action()

    # セッションに会話履歴を保存
    session['chat_history'] = chat_history
    session['all_chat_history'] = all_chat_history

    return jsonify({"message": message, "all_chat_history": all_chat_history})