"""Convert chat emoji shortcodes into Unicode emojis."""


EMOJI_MAP = {
    ":smile:": "😄",
    ":laugh:": "😂",
    ":joy:": "🤣",
    ":love:": "😍",
    ":heart:": "❤️",
    ":wink:": "😉",
    ":sad:": "😢",
    ":cry:": "😭",
    ":angry:": "😠",
    ":surprise:": "😮",
    ":cool:": "😎",
    ":happy:": "😊",
    ":thumbsup:": "👍",
    ":thumbsdown:": "👎",
    ":ok:": "👌",
    ":clap:": "👏",
    ":pray:": "🙏",
    ":fire:": "🔥",
    ":star:": "⭐",
    ":rocket:": "🚀",
    ":100:": "💯",
    ":check:": "✅",
    ":warning:": "⚠️",
    ":coffee:": "☕",
    ":tada:": "🎉",
    ":wave:": "👋",
}


def replace_emojis(message):
    """Replace supported emoji shortcodes with Unicode emojis."""
    for shortcode, emoji in EMOJI_MAP.items():
        message = message.replace(shortcode, emoji)

    return message


if __name__ == "__main__":
    # Simple test for emoji shortcode conversion.
    print(replace_emojis("Hello :smile: :heart: :fire:"))

