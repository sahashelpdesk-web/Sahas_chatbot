from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import requests

app = FastAPI()

# -------------------------------
# STATIC FILES
# -------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------------
# MAKE WEBHOOK
# -------------------------------
MAKE_WEBHOOK = "https://hook.eu2.make.com/j1s4lhtx15uilo5i4dhd8dj6f7x988hm"

# -------------------------------
# GREETING
# -------------------------------
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning ☀️"
    elif hour < 17:
        return "Good afternoon 🌤️"
    return "Good evening 🌙"


def preprocess(text):
    return text.lower().strip()


def is_greeting(text):
    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "gm",
        "gn",
    ]
    return any(text.startswith(x) for x in greetings)


def is_thanks(text):
    return any(x in text for x in ["thanks", "thank you", "thx"])


def is_bye(text):
    return any(x in text for x in ["bye", "goodbye", "see you"])


# -------------------------------
# CALL MAKE AI
# -------------------------------
def ask_make_ai(question):
    try:
        response = requests.post(
            MAKE_WEBHOOK,
            json={
                "message": question
            },
            timeout=60
        )

        if response.status_code == 200:

            # If Make returns JSON
            try:
                data = response.json()

                if "answer" in data:
                    return data["answer"]

                if "reply" in data:
                    return data["reply"]

                if "text" in data:
                    return data["text"]

            except:
                # If Make returns plain text
                return response.text

    except Exception as e:
        print("MAKE ERROR:", e)

    return None


# -------------------------------
# HOME PAGE
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("speak.html", encoding="utf-8") as f:
        return f.read()


# -------------------------------
# CHAT API
# -------------------------------
@app.get("/ask")
def ask(query: str):

    query = preprocess(query)

    # Greeting
    if is_greeting(query):
        return {
            "reply":
                f"{get_greeting()} 👋<br><br>"
                "Welcome to <b>Sahas Support</b> 😊<br><br>"
                "💬 I can help you with:<br>"
                "• HR Queries<br>"
                "• Paybill Issues<br>"
                "• FMS Queries<br><br>"
                "👉 Please type your question."
        }

    # Thanks
    if is_thanks(query):
        return {
            "reply": "You're welcome 😊<br><br>Feel free to ask anything else."
        }

    # Bye
    if is_bye(query):
        return {
            "reply": "Goodbye 👋<br><br>Have a great day!"
        }

    # Ask Make AI
    ai_answer = ask_make_ai(query)

    if ai_answer:
        return {
            "reply":
                "💡 <b>Answer to your query:</b><br><br>"
                + ai_answer +
                "<br><br>"
                "👍 Hope this helps!"
        }

    # Fallback
    return {
        "reply": get_support_template()
    }


# -------------------------------
# SUPPORT TEMPLATE
# -------------------------------
def get_support_template():

    return (
        "<style>"
        ".wa-btn{display:inline-block;background:#25D366;color:white;"
        "padding:10px 16px;border-radius:6px;text-decoration:none;"
        "font-weight:500;}"
        "</style>"

        "Hmm 🤔 I couldn't find an answer.<br><br>"

        "📧 <b>Email Support</b><br>"

        "<a href='mailto:sahas@aiims.edu'>"
        "📩 sahas@aiims.edu"
        "</a><br><br>"

        "<b>HR</b><br>"
        "<a class='wa-btn' href='https://api.whatsapp.com/send?phone=918800155902' target='_blank'>"
        "WhatsApp HR</a><br><br>"

        "<b>Paybill</b><br>"
        "<a class='wa-btn' href='https://api.whatsapp.com/send?phone=918840021359' target='_blank'>"
        "WhatsApp Paybill</a><br><br>"

        "<b>FMS</b><br>"
        "<a class='wa-btn' href='https://api.whatsapp.com/send?phone=919917670730' target='_blank'>"
        "WhatsApp FMS</a>"
    )
