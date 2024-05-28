from flask import request, jsonify, render_template
from app import app
from .chatGPT.action import ChatAction
from .log.log_setting import getMyLogger


chatAction_instance = ChatAction(getMyLogger)


@app.route('/')
def index():
    chat_history = chatAction_instance.first_action()

    return render_template('index.html', chat_history = chat_history)


@app.route('/chat-process', methods=['POST'])
def chat_process():
    user_input = request.get_json()
    user_input = user_input["user_input"]
    chat_history = chatAction_instance.action(user_input)
    
    return jsonify({"chat_history": chat_history})


@app.route('/change-key', methods=['POST'])
def change_key():
    key = request.form['key']
    message = chatAction_instance.change_key(key)
    
    return jsonify({"message": message})