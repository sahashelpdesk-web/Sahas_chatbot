from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from rapidfuzz import fuzz
from datetime import datetime

# ✅ IMPORTANT: define app first
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
        "gm", "gn", "good night",
        "hii", "helo", "hy"
    ]
    return any(greet in query for greet in greetings)

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
                f"{get_greeting()} 👋\n\n"
                "Welcome to *Sahas Support* 😊\n\n"
                "I’m here to help you with:\n"
                "• HR related queries\n"
                "• Paybill issues\n"
                "• FMS concerns\n\n"
                "👉 Please type your question and I’ll assist you."
            )
        }

    # 🙏 Thanks
    if is_thanks(query):
        return {
            "reply": "You're welcome 😊\n\nIf you have any other issue, feel free to ask 👍"
        }

    # 👋 Bye
    if is_bye(query):
        return {
            "reply": "Goodbye 👋\n\nHave a great day ahead! 😊"
        }

    # 🔍 Search KB
    answer = search_kb(query)

    if answer:
        return {"reply": answer}

    # ❌ Fallback
    return {
        "reply": (
            "Hmm 🤔 I couldn’t find an exact answer to your question.\n\n"
            "👉 You can try rephrasing it in a simpler way.\n\n"
            "💡 Example:\n"
            "• 'Employee not showing in salary bill'\n"
            "• 'PFMS file mismatch issue'\n\n"
            "📧 <b>Need more help?</b><br>"
            "<a href='mailto:sahas@aiims.edu?subject=Sahas Support Query&body=Hi Team,' target='_blank'>"
            "Click here to email support</a><br><br>"
            "Our team will assist you shortly.\n\n"
            "<b>For direct queries:</b><br>"
            "• HR: Mr. Pawan<br>"
            "• Paybill: Mr. Divya Mohan<br>"
            "• FMS: Mr. Ankur"
        )
    }
