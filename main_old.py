from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
from rapidfuzz import fuzz
from datetime import datetime

app = FastAPI()

# ✅ STATIC FILES (IMPORTANT FOR IMAGES)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
        return best_match   # ✅ RETURN FULL OBJECT

    return None

# -------------------------------
# 🌐 CHAT UI
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("speak.html", encoding="utf-8") as f:
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
            "reply": "You're welcome 😊<br><br>Feel free to ask anything else 👍"
        }

    # 👋 Bye
    if is_bye(query):
        return {
            "reply": "Goodbye 👋<br><br>Have a great day ahead! 😊"
        }

    # 🔍 Search KB
    answer = search_kb(query)

    if answer:
        reply = (
            "💡 <b>Answer to your query:</b><br><br>"
            f"{answer['answer']}<br><br>"
        )

        # ✅ SHOW IMAGES IF PRESENT
        if "images" in answer:
            for img in answer["images"]:
                reply += f"<img src='{img}' style='max-width:100%;border-radius:8px;margin-top:10px;'/>"

        reply += (
            "<br><br>👍 Hope this helps!<br><br>"
            "<a href='#' onclick='showSupport()' "
            "style='color:#075e54;font-weight:bold;'>👉 Contact Support</a>"
        )

        return {"reply": reply}

    # ❌ Fallback
    return {
        "reply": get_support_template()
    }

# -------------------------------
# 📞 SUPPORT TEMPLATE
# -------------------------------
def get_support_template():
    return (
        "<style>"
        ".wa-btn {"
        "  display: inline-block;"
        "  background-color: #25D366;"
        "  color: white;"
        "  padding: 10px 16px;"
        "  border-radius: 6px;"
        "  text-decoration: none;"
        "  font-weight: 500;"
        "  margin-top: 5px;"
        "}"
        ".wa-btn:hover {"
        "  background-color: #1ebe5d;"
        "}"
        "</style>"

        "Hmm 🤔 I couldn’t find an exact answer to your question.<br><br>"
        "👉 You can try rephrasing it in a simpler way.<br><br>"

        "💡 <b>Examples:</b><br>"
        "• Employee not showing in salary bill<br>"
        "• PFMS file mismatch issue<br><br>"

        "📧 <b>Need more help?</b><br>"
        "<a href='mailto:sahas@aiims.edu?subject=Sahas Support Query&body=Hi Team,' target='_blank'>"
        "📩 Email Support</a><br><br>"

        "📱 <b>Or contact directly on WhatsApp:</b><br><br>"

        "<b>HR</b><br>"
        "<a class='wa-btn' href='https://api.whatsapp.com/send?phone=918800155902' target='_blank'>"
        "💬 Chat on WhatsApp</a><br><br>"

        "<b>Paybill</b><br>"
        "<a class='wa-btn' href='https://api.whatsapp.com/send?phone=918840021359' target='_blank'>"
        "💬 Chat on WhatsApp</a><br><br>"

        "<b>FMS</b><br>"
        "<a class='wa-btn' href='https://api.whatsapp.com/send?phone=919917670730' target='_blank'>"
        "💬 Chat on WhatsApp</a><br><br>"

        "Our team will assist you shortly 😊"
    )
