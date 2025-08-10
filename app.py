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
        "user_avatar": "/static/user.png",
        "model": "llama3"
    }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

@app.route("/")
def index():
    config = load_config()
    return render_template("index.html", config=config)

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    user_message = data.get("message", "")

    config = load_config()
    model = config.get("model", "llama3")

    # Call Ollama
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": user_message}]
    )
    ai_reply = response["message"]["content"]

    return jsonify({
        "reply": ai_reply,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })

@app.route("/update_settings", methods=["POST"])
def update_settings():
    data = request.form
    config = load_config()
    config["bot_name"] = data.get("bot_name", config["bot_name"])
    config["bot_avatar"] = data.get("bot_avatar", config["bot_avatar"])
    config["user_avatar"] = data.get("user_avatar", config["user_avatar"])
    save_config(config)
    return "Settings updated", 200

if __name__ == "__main__":
    app.run(debug=True)
