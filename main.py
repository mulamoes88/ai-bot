
from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Zet je OpenAI API key hier
OPENAI_API_KEY = "sk-...JOUW_SLEUTEL..."

# Telegram bot configuratie
TELEGRAM_TOKEN = "8210264778:AAEhh_IxGx60WI_KOIwrr3LaFGcJF4M00Kw"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.get("/")
def root():
    return {"status": "Bot backend actief"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    return {"response": answer}


@app.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    message = data.get("message")
    if not message:
        return {"status": "no message"}

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # Stuur naar eigen backend
    response = requests.post("https://ai-bot-60c6.onrender.com/chat", json={"message": text})
    bot_reply = response.json().get("response", "Ik snap je niet helemaal.")

    # Antwoord naar Telegram
    send_url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": bot_reply}
    requests.post(send_url, json=payload)

    return {"status": "ok"}
