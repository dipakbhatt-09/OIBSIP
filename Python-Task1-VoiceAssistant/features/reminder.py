import re
import threading
import time


def reminder_alert(message, seconds, speak):

    time.sleep(seconds)

    speak(
        f"Reminder: {message}"
    )


def set_reminder(command, speak):

    numbers = re.findall(
        r"\d+",
        command
    )

    if not numbers:

        speak(
            "Please tell me the reminder time in seconds."
        )

        return

    seconds = int(numbers[0])

    message = "Your reminder time is over."

    if "to" in command:

        message = command.split(
            "to",
            1
        )[1].strip()

    speak(
        f"Okay. I will remind you after "
        f"{seconds} seconds."
    )

    reminder_thread = threading.Thread(
        target=reminder_alert,
        args=(
            message,
            seconds,
            speak
        )
    )

    reminder_thread.daemon = True

    reminder_thread.start()