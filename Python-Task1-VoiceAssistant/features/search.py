import webbrowser

def search_web(command, speak):

    topic = command

    for phrase in [
        "search",
        "google",
        "find",
        "look up"
    ]:
        topic = topic.replace(
            phrase,
            ""
        ).strip()

    if topic:

        speak(
            f"Searching for {topic}"
        )

        webbrowser.open(
            f"https://www.google.com/search?q={topic}"
        )

    else:

        speak(
            "Please tell me what you want me to search for."
        )