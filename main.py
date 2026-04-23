from fastapi import FastAPI
import json
import requests
from rapidfuzz import fuzz

app = FastAPI()

with open("kb.json", encoding="utf-8") as f:
    KB = json.load(f)

GROQ_API_KEY = "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"

# 🔍 SMART SEARCH
def search_kb(query):
    query = query.lower()
    best_match = None
    best_score = 0

    for item in KB:
        score = fuzz.partial_ratio(query, item["question"])
        if score > best_score:
            best_score = score
            best_match = item

    if best_score > 60:
        return best_match["answer"]
    else:
        return "No exact match found in KB."

# 🤖 GROQ CALL (ONLY ONCE)
def ask_groq(query, context):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "Answer ONLY from context. Be short."},
            {"role": "user", "content": f"Question: {query}\nContext: {context}"}
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]

@app.get("/ask")
def ask(query: str):
    context = search_kb(query)

    # 🔥 ONLY 1 CREDIT USED HERE
    answer = ask_groq(query, context)

    return {"answer": answer}