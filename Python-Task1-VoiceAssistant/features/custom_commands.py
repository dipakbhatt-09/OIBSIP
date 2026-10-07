import json
import os


CUSTOM_COMMANDS_FILE = (
    "data/commands.json"
)


def load_custom_commands():

    if not os.path.exists(
        CUSTOM_COMMANDS_FILE
    ):
        return {}

    try:

        with open(
            CUSTOM_COMMANDS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


def save_custom_command(
    command,
    response
):

    commands = load_custom_commands()

    commands[command] = response

    with open(
        CUSTOM_COMMANDS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            commands,
            file,
            indent=4
        )




def check_custom_command(
    command,
    speak
):

    commands = load_custom_commands()

    for custom_command, response in commands.items():

        if custom_command in command:

            speak(response)

            return True

    return False


def add_custom_command(
    listen,
    speak
):

    speak(
        "Tell me the custom command."
    )

    command = listen()

    if not command:
        return

    speak(
        "Tell me what I should say when "
        "you use this command."
    )

    response = listen()

    if not response:
        return

    save_custom_command(
        command,
        response
    )

    speak(
        "Your custom command has been saved."
    )