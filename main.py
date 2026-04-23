from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from rapidfuzz import fuzz

app = FastAPI()

# Load KB
with open("kb.json", encoding="utf-8") as f:
    KB = json.load(f)

# -------------------------------
# 🔧 PREPROCESS
# -------------------------------
def preprocess(query):
    return query.lower().strip()

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

    if best_score >= 70:
        return best_match["answer"]

    return None

# -------------------------------
# 🌐 CHAT UI
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()

# -------------------------------
# 🤖 CHAT API
# -------------------------------
@app.get("/ask")
def ask(query: str):
    query = preprocess(query)

    # greetings
    if query in ["hi", "hello", "hey"]:
        return {"reply": "Hi 👋\nHow can I help you today?"}

    answer = search_kb(query)

    if answer:
        return {"reply": f"{answer}"}

    return {"reply": "I couldn’t find that 🤔\nPlease rephrase your question."}
