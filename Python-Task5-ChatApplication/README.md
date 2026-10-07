# Chat Application

A real-time desktop chat application built with Python and Tkinter. The application supports user authentication, multiple chat rooms, message history, emoji shortcodes, and notifications when new messages arrive while the application window is not focused.

## Features

* User registration and login
* Password hashing before storing credentials
* Real-time messaging using Python TCP sockets
* Multiple chat rooms
* Create and join chat rooms
* Message history for each room
* SQLite database for persistent data storage
* Emoji shortcode support such as `:smile:` and `:heart:`
* Notification when a new message arrives while the window is unfocused
* Simple and responsive Tkinter GUI

## Technologies Used

* Python
* Tkinter
* SQLite
* TCP Sockets
* Threading
* hashlib

## Project Structure

```text
Python-Task5-ChatApplication/
│
├── server/
│   ├── __init__.py
│   ├── server.py
│   ├── database.py
│   └── auth.py
│
├── client/
│   ├── __init__.py
│   ├── client.py
│   ├── gui.py
│   └── emoji.py
│
├── data/
│   └── chat.db
│
├── README.md
├── requirements.txt
└── .gitignore
```

## How It Works

The application uses a client-server architecture.

The server listens for TCP connections on:

```text
127.0.0.1:5000
```

The Tkinter client connects to the server and sends or receives messages through the socket connection.

A background thread continuously receives messages from the server so that the GUI remains responsive.

## Database

SQLite is used to store application data in:

```text
data/chat.db
```

The database contains three main tables:

### Users

Stores registered user accounts.

* `id`
* `username`
* `password`

Passwords are not stored as plain text. The current implementation stores a SHA-256 hash of the password.

### Rooms

Stores available chat rooms.

* `id`
* `name`

A `General` room is created automatically when the database is initialized.

### Messages

Stores chat messages for each room.

* `id`
* `room_id`
* `username`
* `message`
* `timestamp`

Messages are stored as plain text in the SQLite database.

## Security and Encryption

This project is created as an internship learning project and is not intended for production use.

* User passwords are stored as SHA-256 hashes instead of plain-text passwords.
* Messages are stored as plain text in SQLite.
* Chat communication is currently sent through a normal TCP socket without TLS encryption.
* The application does not provide end-to-end encryption.
* Sensitive production applications should use stronger password-hashing methods and encrypted network communication.

## Emoji Support

The application supports emoji shortcodes.

Examples:

```text
:smile:     → 😄
:heart:     → ❤️
:fire:      → 🔥
:thumbsup:  → 👍
:tada:      → 🎉
```

Emoji conversion is handled by:

```text
client/emoji.py
```

## Requirements

* Python 3.10 or newer
* Tkinter
* No external database server is required because SQLite is included with Python.

## Installation

Clone or download the project and open the project directory:

```powershell
cd Python-Task5-ChatApplication
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

## Running the Application

### Step 1: Start the Server

Open a terminal and run:

```powershell
python server\server.py
```

The server should display:

```text
Chat server started.
Listening on 127.0.0.1:5000
Waiting for clients...
```

### Step 2: Start the Client

Open another terminal and run:

```powershell
python client\gui.py
```

### Step 3: Register and Login

1. Enter a username and password.
2. Click **Register**.
3. Login using the registered account.
4. Join the `General` room or create another room.
5. Start chatting.

## Chat Commands

The application supports the following server commands:

```text
/rooms
/create room_name
/join room_name
/register username password
/login username password
```

Most of these commands are handled through the graphical interface.

## Message History

When a user joins a room, the application retrieves previously stored messages from the SQLite database.

The latest 50 messages are loaded for the selected room.

## Notifications

When a new message arrives while the application window is not focused, the application:

* Plays the Tkinter notification sound.
* Changes the window title to indicate a new message.

## Limitations

This project has some limitations because it is designed for learning purposes:

* The server currently runs on the local machine.
* Network communication is not encrypted with TLS.
* Messages are stored as plain text.
* The password hashing implementation uses SHA-256 and does not use a salt.
* The notification system uses the Tkinter window bell and title change rather than a native operating-system notification.
* The application is not designed for production deployment.

## Learning Objectives

This project demonstrates practical use of:

* Python socket programming
* Client-server architecture
* Multithreading
* Tkinter GUI development
* SQLite database operations
* User authentication
* Password hashing
* Real-time communication
* Room-based messaging
* Message persistence
* Emoji processing
* Basic desktop notifications

## Internship Task

**Oasis Infobyte AICTE SIP Internship**

**Track:** Python Programming

**Task:** Chat Application

**Level:** Advanced
