import speech_recognition as sr
import pyttsx3

from datetime import datetime
from dotenv import load_dotenv


# LOAD ENVIRONMENT VARIABLES
load_dotenv()

# IMPORT FEATURES
from features.search import search_web
from features.weather import get_weather
from features.reminder import set_reminder
from features.email import send_email
from features.knowledge import answer_question
from features.custom_commands import (
    check_custom_command,
    add_custom_command,
)


# VOICE ASSISTANT
class VoiceAssistant:

    def __init__(self):

       
        # Speech Recognition
        self.recognizer = sr.Recognizer()

        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.5
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300

    # VOICE RESPONSE
    def speak(self, text):

        print("Assistant:", text)

        try:

            engine = pyttsx3.init()

            engine.setProperty(
                "rate",
                170
            )

            engine.setProperty(
                "volume",
                1.0
            )

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as error:

            print(
                "Text-to-speech error:",
                error
            )

    # VOICE INPUT
    def listen(self):

        try:

            with sr.Microphone() as source:

                print("\nListening...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=None,
                    phrase_time_limit=8
                )

            text = self.recognizer.recognize_google(
                audio,
                language="en-US"
            )

            print(
                "You said:",
                text
            )

            return text.lower().strip()

        except sr.UnknownValueError:

            self.speak(
                "Sorry, I could not understand you. "
                "Please repeat."
            )

            return ""

        except sr.RequestError:

            self.speak(
                "Speech recognition service is unavailable."
            )

            return ""

        except Exception as error:

            print(
                "Voice recognition error:",
                error
            )

            self.speak(
                "Something went wrong with voice recognition."
            )

            return ""


    # INTENT DETECTION
    def get_intent(self, command):

        command = command.lower().strip()

        exit_phrases = [
            "exit",
            "quit",
            "stop",
            "goodbye",
            "good bye",
            "bye",
            "close assistant",
            "shutdown assistant",
        ]

        if any(
            phrase in command
            for phrase in exit_phrases
        ):

            return "exit"


        # CUSTOM COMMAND
        if any(
            phrase in command
            for phrase in [
                "add custom command",
                "create custom command",
                "new custom command",
                "add a custom command",
                "create a custom command",
            ]
        ):

            return "custom"


        # EMAIL
        if any(
            phrase in command
            for phrase in [
                "send email",
                "send an email",
                "send a mail",
                "send mail",
                "email someone",
                "send an email to",
                "write an email",
            ]
        ):

            return "email"


        # WEATHER
        if any(
            phrase in command
            for phrase in [
                "weather",
                "temperature",
                "forecast",
                "how hot is",
                "how cold is",
                "weather like",
                "temperature like",
            ]
        ):

            return "weather"


        # REMINDER
        if any(
            phrase in command
            for phrase in [
                "remind me",
                "reminder",
                "set a reminder",
                "set reminder",
                "remind me after",
                "remind me in",
            ]
        ):

            return "reminder"


        # SEARCH
        if any(
            phrase in command
            for phrase in [
                "search",
                "google",
                "look up",
                "find information",
                "search for",
                "look for",
                "find out",
            ]
        ):

            return "search"


        # TIME
        time_phrases = [
            "what time is it",
            "what is the time",
            "what's the time",
            "tell me the time",
            "tell me what time it is",
            "could you tell me the time",
            "can you tell me the time",
            "would you tell me the time",
            "do you know the time",
            "current time",
            "time right now",
            "what time is it right now",
        ]

        if any(
            phrase in command
            for phrase in time_phrases
        ):

            return "time"

        words = command.split()

        if (
            "time" in words
            and any(
                word in words
                for word in [
                    "tell",
                    "know",
                    "current",
                    "right",
                    "now",
                ]
            )
        ):

            return "time"


        # DATE
        date_phrases = [
            "what is today's date",
            "what's today's date",
            "what is the date",
            "what's the date",
            "tell me today's date",
            "tell me the date",
            "what day is it",
            "what day is today",
            "today's date",
            "current date",
            "date today",
        ]

        if any(
            phrase in command
            for phrase in date_phrases
        ):

            return "date"

        if (
            "date" in words
            and any(
                word in words
                for word in [
                    "tell",
                    "know",
                    "current",
                    "today",
                ]
            )
        ):

            return "date"


        # GREETING
        greeting_words = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
        ]

        if any(
            phrase in command
            for phrase in greeting_words
        ):

            return "hello"


        # GENERAL KNOWLEDGE
        knowledge_phrases = [
            "who is",
            "who was",
            "what is",
            "what are",
            "what was",
            "where is",
            "where was",
            "when was",
            "when is",
            "which",
            "why is",
            "why was",
            "why does",
            "why do",
            "how is",
            "how does",
            "how do",
            "how can",
            "tell me about",
            "can you tell me",
            "could you tell me",
            "please tell me",
            "i want to know",
            "i would like to know",
            "do you know about",
        ]

        if any(
            phrase in command
            for phrase in knowledge_phrases
        ):

            return "knowledge"


        # UNKNOWN
        return "unknown"


    # MAIN PROGRAM
    def run(self):

        self.speak(
            "Hello! I am your voice assistant. "
            "How can I help you?"
        )

        while True:

            command = self.listen()

            if not command:
                continue


            # CUSTOM COMMANDS FIRST
            if check_custom_command(
                command,
                self.speak
            ):

                continue


            # DETECT INTENT
            intent = self.get_intent(
                command
            )


            # GREETING
            if intent == "hello":

                self.speak(
                    "Hello! How can I help you?"
                )


            # TIME
            elif intent == "time":

                current_time = datetime.now().strftime(
                    "%I:%M %p"
                )

                self.speak(
                    f"The current time is {current_time}."
                )


            # DATE
            elif intent == "date":

                current_date = datetime.now().strftime(
                    "%B %d, %Y"
                )

                self.speak(
                    f"Today's date is {current_date}."
                )


            # SEARCH
            elif intent == "search":

                search_web(
                    command,
                    self.speak
                )


            # REMINDER
            elif intent == "reminder":

                set_reminder(
                    command,
                    self.speak
                )


            # WEATHER
            elif intent == "weather":

                get_weather(
                    command,
                    self.speak
                )


            # EMAIL
            elif intent == "email":

                send_email(
                    self.listen,
                    self.speak
                )


            # GENERAL KNOWLEDGE
            elif intent == "knowledge":

                answer_question(
                    command,
                    self.speak
                )


            # CUSTOM COMMAND
            elif intent == "custom":

                add_custom_command(
                    self.listen,
                    self.speak
                )


            # EXIT
            elif intent == "exit":

                self.speak(
                    "Goodbye! Have a nice day."
                )

                break


            # UNKNOWN COMMAND
            else:

                self.speak(
                    "Sorry, I don't understand that command. "
                    "Please try again."
                )



# START APPLICATION
if __name__ == "__main__":

    assistant = VoiceAssistant()

    assistant.run()