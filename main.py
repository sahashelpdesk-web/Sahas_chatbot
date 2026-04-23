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
            "reply": (
                "You're welcome 😊\n\n"
                "If you have any other issue, feel free to ask 👍"
            )
        }

    # 👋 Bye
    if is_bye(query):
        return {
            "reply": (
                "Goodbye 👋\n\n"
                "Have a great day ahead! 😊"
            )
        }

    # 🔍 Search KB
    answer = search_kb(query)

    if answer:
        return {
            "reply": answer
        }

    # ❌ Friendly fallback
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
