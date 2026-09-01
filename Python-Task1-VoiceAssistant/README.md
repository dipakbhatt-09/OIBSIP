## Privacy & Data Processing

This voice assistant processes spoken commands through the microphone
and converts speech to text using Google's speech recognition service.

The application may process:

- Voice input from the microphone
- Text commands entered through speech recognition
- Weather requests sent to OpenWeatherMap
- Email credentials stored in environment variables
- Email messages sent through Gmail SMTP
- Custom commands stored locally in `commands.json`

Sensitive credentials such as API keys, email addresses, and passwords
are stored in the `.env` file and should not be committed to GitHub.

The `.env` file is included in `.gitignore`.

The application does not intentionally store raw microphone recordings.