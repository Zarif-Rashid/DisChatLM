from flask import Flask, request, jsonify, render_template
import ollama
import json
import os
from datetime import datetime

app = Flask(__name__)

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "bot_name": "AI Friend",
        "bot_avatar": "/static/default_bot.png",
        "user_name": "You",
        "user_avatar": "/static/user.png",
        "model": "llama3",
        "response_delay": 6,
        "inactivity_timeout": 30
    }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

@app.route("/")
def index():
    config = load_config()
    return render_template("index.html", config=config)

# Global conversation history
conversation_history = []

@app.route("/send_message", methods=["POST"])
def send_message():
    global conversation_history
    data = request.json
    user_message = data.get("message", "")

    config = load_config()
    model = config.get("model", "llama3")
    response_delay = config.get("response_delay", 6)
    system_prompt = config.get("system_prompt", "You are a helpful, friendly AI assistant.")

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_message})
    
    # Keep only the last 20 messages to prevent context from getting too long
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    # Build messages with system prompt and conversation history
    messages = [{"role": "system", "content": system_prompt}] + conversation_history

    # Call Ollama with conversation history
    response = ollama.chat(
        model=model,
        messages=messages
    )
    ai_reply = response["message"]["content"]
    
    # Add AI response to history
    conversation_history.append({"role": "assistant", "content": ai_reply})

    # Add artificial delay
    import time
    time.sleep(response_delay)

    return jsonify({
        "reply": ai_reply,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })

@app.route("/inactivity_message", methods=["POST"])
def inactivity_message():
    global conversation_history
    data = request.json
    last_message = data.get("last_message", "")
    
    config = load_config()
    model = config.get("model", "llama3")
    system_prompt = config.get("system_prompt", "You are a helpful, friendly AI assistant.")
    
    # Create context-aware inactivity message
    context = f"User's last message was: '{last_message}'. They haven't responded for a while. Send a brief, friendly message to re-engage them while staying on topic, continuing your last message. Keep it concise and friendly"
    
    # Build messages with system prompt and conversation history
    messages = [{"role": "system", "content": system_prompt}] + conversation_history + [{"role": "user", "content": context}]
    
    response = ollama.chat(
        model=model,
        messages=messages
    )
    inactivity_reply = response["message"]["content"]
    
    # Add inactivity message to history
    conversation_history.append({"role": "user", "content": context})
    conversation_history.append({"role": "assistant", "content": inactivity_reply})
    
    return jsonify({
        "reply": inactivity_reply,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })

@app.route("/clear_history", methods=["POST"])
def clear_history():
    global conversation_history
    conversation_history = []
    return jsonify({"message": "Conversation history cleared"}), 200

@app.route("/update_settings", methods=["POST"])
def update_settings():
    data = request.form
    config = load_config()
    config["bot_name"] = data.get("bot_name", config["bot_name"])
    config["bot_avatar"] = data.get("bot_avatar", config["bot_avatar"])
    config["user_name"] = data.get("user_name", config["user_name"])
    config["user_avatar"] = data.get("user_avatar", config["user_avatar"])
    config["response_delay"] = int(data.get("response_delay", config["response_delay"]))
    config["inactivity_timeout"] = int(data.get("inactivity_timeout", config["inactivity_timeout"]))
    config["system_prompt"] = data.get("system_prompt", config.get("system_prompt", "You are a helpful, friendly AI assistant."))
    save_config(config)
    return "Settings updated", 200

if __name__ == "__main__":
    app.run(debug=True)
