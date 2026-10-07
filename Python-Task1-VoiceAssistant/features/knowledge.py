import webbrowser

def answer_question(command, speak):

    question = command

    for phrase in [
        "who is",
        "what is",
        "what are",
        "where is",
        "when was",
        "tell me about"
    ]:

        question = question.replace(
            phrase,
            ""
        ).strip()

    if not question:

        speak(
            "Please tell me what you want to know."
        )

        return

    speak(
        f"Searching for information about {question}"
    )

    webbrowser.open(
        f"https://www.google.com/search?q={question}"
    )