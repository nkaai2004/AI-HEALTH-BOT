from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import sympy as sp
import json

app = Flask(__name__)

# Load custom health-related training data
with open('health_data.json') as f:
    health_data = json.load(f)

chatbot = ChatBot("HealthBot")
trainer = ListTrainer(chatbot)

# Train the chatbot with custom data
trainer.train(health_data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("message")
    response = chatbot.get_response(user_input)
    return jsonify({"response": str(response)})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    expr = request.json.get("expression")
    result = sp.sympify(expr)
    return jsonify({"result": str(result)})

@app.route('/clear', methods=['POST'])
def clear():
    chatbot.storage.drop()
    return jsonify({"message": "Chat history cleared."})

@app.route('/help', methods=['GET'])
def help():
    help_message = """
    Available Commands:
    1. Ask health-related questions
    2. Evaluate mathematical expressions
    3. Clear chat history
    4. Greet and Farewell
    """
    return jsonify({"help": help_message})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add code here to handle the registration logic, such as saving to a database
        return jsonify({"message": "Registration successful!"})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add code here to handle the login logic, such as checking the database
        return jsonify({"message": "Login successful!"})
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Change port to 5001
