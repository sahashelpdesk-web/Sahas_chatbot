from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from rapidfuzz import fuzz
from datetime import datetime

app = FastAPI()

# -------------------------------
# 📂 LOAD KB
# -------------------------------
with open("kb.json", encoding="utf-8") as f:
    KB = json.load(f)

# -------------------------------
# 🔧 PREPROCESS
# -------------------------------
def preprocess(query):
    return query.lower().strip()

# -------------------------------
# 👋 GREETING LOGIC
# -------------------------------
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning ☀️"
    elif hour < 17:
        return "Good afternoon 🌤️"
    else:
        return "Good evening 🌙"

def is_greeting(query):
    greetings = [
        "hi", "hello", "hey",
        "good morning", "good afternoon", "good evening",
        "gm", "gn", "good night"
    ]
    return any(query.startswith(greet) for greet in greetings)

def is_thanks(query):
    return any(word in query for word in ["thanks", "thank you", "thx"])

def is_bye(query):
    return any(word in query for word in ["bye", "goodbye", "see you"])

# -------------------------------
# 🔍 SMART SEARCH
# -------------------------------
def search_kb(query):
    best_match = None
    best_score = 0

    for item in KB:
        q = item["question"].lower()

        score = (
            fuzz.partial_ratio(query, q) +
            fuzz.token_sort_ratio(query, q) +
            fuzz.token_set_ratio(query, q)
        ) / 3

        if score > best_score:
            best_score = score
            best_match = item

    if best_score >= 65:
        return best_match["answer"]

    return None

# -------------------------------
# 🌐 CHAT UI
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", encoding="utf-8") as f:
        return f.read()

# -------------------------------
# 🤖 CHAT API
# -------------------------------
@app.get("/ask")
def ask(query: str):
    query = preprocess(query)

    # 👋 Greeting
    if is_greeting(query):
        return {
            "reply": (
                f"{get_greeting()} 👋<br><br>"
                "Welcome to <b>Sahas Support</b> 😊<br><br>"
                "💬 I can help you with:<br>"
                "• HR queries<br>"
                "• Paybill issues<br>"
                "• FMS concerns<br><br>"
                "👉 Please type your question."
            )
        }

    # 🙏 Thanks
    if is_thanks(query):
        return {
            "reply": (
                "You're welcome 😊<br><br>"
                "If you have any other issue, feel free to ask 👍"
            )
        }

    # 👋 Bye
    if is_bye(query):
        return {
            "reply": (
                "Goodbye 👋<br><br>"
                "Have a great day ahead! 😊"
            )
        }

    # 🔍 Search KB
    answer = search_kb(query)

    if answer:
        return {
            "reply": (
                "💡 <b>Answer to your query:</b><br><br>"
                f"{answer}<br><br>"
                "👍 Hope this helps!<br>"
                "If not, you can ask again or contact support."
            )
        }

    # ❌ Fallback
    return {
        "reply": (
            "Hmm 🤔 I couldn’t find an exact answer to your question.<br><br>"
            "👉 You can try rephrasing it in a simpler way.<br><br>"

            "💡 <b>Examples:</b><br>"
            "• Employee not showing in salary bill<br>"
            "• PFMS file mismatch issue<br><br>"

            "📧 <b>Need more help?</b><br>"
            "<a href='mailto:sahas@aiims.edu?subject=Sahas Support Query&body=Hi Team,' target='_blank'>"
            "📩 Email Support</a><br><br>"

            "📱 <b>Or contact directly on WhatsApp:</b><br><br>"

            "• HR (Mr. Pawan): "
            "<a href='https://api.whatsapp.com/send?phone=918800155902&text=Hi%20Pawan%20Sir,%20I%20have%20an%20HR%20query%20from%20Sahas%20chatbot' target='_blank'>"
            "8800155902</a><br>"

            "• Paybill (Mr. Divya Mohan): "
            "<a href='https://api.whatsapp.com/send?phone=918840021359&text=Hi%20Sir,%20I%20have%20a%20Paybill%20query%20from%20Sahas%20chatbot' target='_blank'>"
            "8840021359</a><br>"

            "• FMS (Mr. Ankur): "
            "<a href='https://api.whatsapp.com/send?phone=919917670730&text=Hi%20Sir,%20I%20have%20an%20FMS%20query%20from%20Sahas%20chatbot' target='_blank'>"
            "9917670730</a><br><br>"

            "Our team will assist you shortly 😊"
        )
    }
