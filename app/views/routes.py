from flask import request, jsonify, render_template
from app import app
from chatbot import ChatBot

chatbot_instance = ChatBot()

@app.route('/')
def index():
    chat_history = chatbot_instance.first_action()

    return render_template('index.html', chat_history = chat_history)

@app.route('/chat-process', methods=['POST'])
def chat():
    user_input = request.get_json()
    user_input = user_input["user_input"]
    chat_history = chatbot_instance.action(user_input)
    
    return jsonify({"chat_history": chat_history})

@app.route('/change-key', methods=['POST'])
def chat():
    key = request.form['key']
    message = chatbot_instance.change_key(key)
    
    return jsonify({"message": message})