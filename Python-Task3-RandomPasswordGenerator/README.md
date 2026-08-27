# Random Password Generator

A Python-based random password generator that creates strong and secure passwords based on user-selected criteria.

## Features

### Beginner Version
- Set password length with a minimum of 8 characters
- Choose uppercase letters, lowercase letters, numbers, and symbols
- Requires at least 2 character types
- Generates a secure random password
- Displays password strength
- Allows generating another password without restarting

### Advanced Version
- User-friendly Tkinter GUI
- Password length control using a Spinbox
- Character type selection using checkboxes
- Uses Python's `secrets` module for secure password generation
- Guarantees at least one character from each selected type
- Password strength indicator
- Automatically copies generated passwords to the clipboard
- Copy to Clipboard button
- Option to exclude ambiguous characters
- Displays the last 5 generated passwords during the session

## Technologies Used

- Python
- Tkinter
- secrets
- string
- pyperclip

## Project Files

- `main.py` - Command-line version of the password generator
- `gui.py` - Advanced GUI version of the password generator
- `requirements.txt` - Required external Python package
- `.gitignore` - Files and folders excluded from Git
- `README.md` - Project documentation

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv