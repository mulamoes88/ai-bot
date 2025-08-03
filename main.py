
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Zet je eigen API-sleutels hier
OPENAI_API_KEY = "sk-proj-..."  # ← vul jouw volledige OpenAI key in
TELEGRAM_TOKEN = "8210264778:AAEhh_IxGx60WI_KOIwrr3LaFGcJF4M00Kw"  # ← jouw Telegram bot token

@app.route("/", methods=["GET"])
def home():
    return jsonify(status="Bot backend actief")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    json_data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = "Fout bij ophalen van GPT antwoord."

    return jsonify(reply=reply)

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    message = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id", "")

    # GPT-aanroep
    gpt_response = requests.post(
        "https://ai-bot-60c6.onrender.com/chat",
        json={"message": message}
    )
    gpt_reply = gpt_response.json().get("reply", "Geen antwoord ontvangen.")

    # Stuur naar Telegram terug
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(telegram_url, json={
        "chat_id": chat_id,
        "text": gpt_reply
    })

    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
