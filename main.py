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

        score1 = fuzz.partial_ratio(query, q)
        score2 = fuzz.token_sort_ratio(query, q)
        score3 = fuzz.token_set_ratio(query, q)

        score = (score1 + score2 + score3) / 3

        if score > best_score:
            best_score = score
            best_match = item

    if best_score >= 65:   # slightly relaxed for better matching
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
                "Welcome to Sahas Support.\n\n"
                "I can help you with:\n"
                "• HR queries\n"
                "• Paybill issues\n"
                "• FMS queries\n\n"
                "Please tell me your issue 😊"
            )
        }

    # 🙏 Thanks
    if is_thanks(query):
        return {
            "reply": "You're welcome 😊\nLet me know if you need any further assistance!"
        }

    # 👋 Bye
    if is_bye(query):
        return {
            "reply": "Goodbye 👋\nHave a great day!"
        }

    # 🔍 Search KB
    answer = search_kb(query)

    if answer:
        return {
            "reply": f"{answer}"
        }
        # 🔍 Search KB
answer = search_kb(query)

if answer:
    return {
        "reply": f"{answer}"
    }


return {
    "reply": (
        "Hmm 🤔 I couldn’t find an exact answer.<br><br>"
        "Please try rephrasing your question.<br><br>"
        "📧 <b>Email us:</b> "
        "<a href='mailto:sahas@aiims.edu?subject=Sahas Support Query&body=Hi Team,' target='_blank'>sahas@aiims.edu</a><br><br>"
        "Our team will resolve your query.<br><br>"
        "<b>For specific queries:</b><br>"
        "• HR: Mr. Pawan<br>"
        "• Paybill: Mr. Divya Mohan<br>"
        "• FMS: Mr. Ankur"
    )
}


