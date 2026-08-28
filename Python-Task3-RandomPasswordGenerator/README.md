# Random Password Generator

A Python project for generating random and secure passwords. It includes a simple command-line version and a Tkinter desktop GUI.

## Features

### Command-Line Version

* Set password length with a minimum of 8 characters
* Choose uppercase letters, lowercase letters, numbers, and symbols
* Requires at least 2 character types
* Generates a secure random password
* Shows password length and password strength
* Allows generating another password without restarting
* Uses Python's `secrets` module

### GUI Version

* Simple Tkinter desktop interface
* Set password length from 8 to 100 characters
* Select uppercase letters, lowercase letters, numbers, and symbols
* Requires at least 2 character types
* Option to exclude ambiguous characters such as `0`, `O`, `l`, and `1`
* Uses `secrets` for secure password generation
* Ensures at least one character from each selected type
* Shows password strength
* Automatically copies the generated password to the clipboard
* Copy to Clipboard button
* Shows the last 5 generated passwords

## Technologies Used

* Python
* Tkinter
* secrets
* string
* pyperclip

## Project Files

* `main.py` - Command-line version of the password generator
* `gui.py` - Tkinter GUI version of the password generator
* `requirements.txt` - Required Python package
* `.gitignore` - Files excluded from Git
* `README.md` - Project documentation

## Installation

1. Create a virtual environment:

   `python -m venv venv`

2. Activate the virtual environment on Windows:

   `venv\Scripts\activate`

3. Install the required package:

   `pip install -r requirements.txt`

## How to Run

For the command-line version:

`python main.py`

For the GUI version:

`python gui.py`

## How It Works

The user selects the password length and character types. The program generates a password using Python's `secrets` module.

The GUI version also provides password strength information, clipboard copying, ambiguous character filtering, and a history of the last 5 generated passwords.

## Project Purpose

This project was created as part of the Oasis Infobyte Python Programming Internship to practice Python programming, secure password generation, input validation, and Tkinter GUI development.
