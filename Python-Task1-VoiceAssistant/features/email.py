import smtplib
import os


# EMAIL SETTINGS
EMAIL_ADDRESS = os.getenv("ASSISTANT_EMAIL")
EMAIL_PASSWORD = os.getenv("ASSISTANT_EMAIL_PASSWORD")



# CONVERT VOICE EMAIL
def clean_email_address(text):
    """Convert spoken email address into a normal email address."""

    email = text.lower().strip()

    
    email = email.replace(" at ", "@")
    email = email.replace(" at", "@")
    email = email.replace("at ", "@")

    email = email.replace(" dot ", ".")
    email = email.replace(" dot", ".")
    email = email.replace("dot ", ".")

   
    email = email.replace(" gmail ", "@gmail.com")
    email = email.replace(" gmail", "@gmail.com")
    email = email.replace("gmail.com", "@gmail.com")

    
    email = email.replace(" ", "")

    return email



# SEND EMAIL 
def send_email(listen, speak):

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:

        speak(
            "Email settings are not configured."
        )

        return

    speak(
        "Please tell me the recipient email address. "
        "For example, say dipak at gmail dot com."
    )

    recipient = listen()

    if not recipient:
        return

    # Convert spoken email into proper email format
    recipient = clean_email_address(recipient)

    print("Email recipient:", recipient)


    # Confirm the address before sending
    speak(
        f"I understood the recipient as {recipient}. "
        "Is that correct? Please say yes or no."
    )

    confirmation = listen()

    if not confirmation:
        return

    if "yes" not in confirmation:

        speak(
            "Okay. The email was cancelled."
        )

        return

    speak(
        "Please tell me the email message."
    )

    message = listen()

    if not message:
        return

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            email_text = (
                "Subject: Voice Assistant Message\n\n"
                f"{message}"
            )

            server.sendmail(
                EMAIL_ADDRESS,
                recipient,
                email_text
            )

        speak(
            "The email has been sent successfully."
        )

    except Exception as error:

        print(
            "Email error:",
            error
        )

        speak(
            "Sorry, I could not send the email."
        )