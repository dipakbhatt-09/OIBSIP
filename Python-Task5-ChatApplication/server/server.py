"""TCP chat server with authentication, rooms, and message history."""

import socket
import threading
from datetime import datetime

from auth import login_user, register_user
from database import (
    create_room as db_create_room,
    get_message_history,
    get_rooms,
    initialize_database,
    room_exists,
    save_message,
)


HOST = "127.0.0.1"
PORT = 5000

clients = {}

rooms = {
    "General": set()
}

# Protect shared client and room data from concurrent access.
clients_lock = threading.Lock()


def get_timestamp():
    """Return the current time in HH:MM format."""
    return datetime.now().strftime("%H:%M")


def send_message(client_socket, message):
    """Send a UTF-8 message to a connected client."""
    try:
        client_socket.sendall(
            (message + "\n").encode("utf-8")
        )
        return True

    except (
        ConnectionResetError,
        BrokenPipeError,
        OSError
    ):
        return False


def broadcast_to_room(room_name, message, sender_socket=None):
    """Send a message to all clients currently in a room."""
    with clients_lock:
        room_clients = rooms.get(
            room_name,
            set()
        ).copy()

    disconnected_clients = []

    for client_socket in room_clients:
        # Do not send the message back to its sender.
        if client_socket == sender_socket:
            continue

        if not send_message(
            client_socket,
            message
        ):
            disconnected_clients.append(
                client_socket
            )

    # Remove clients whose connections are no longer active.
    if disconnected_clients:
        with clients_lock:
            for client_socket in disconnected_clients:
                clients.pop(
                    client_socket,
                    None
                )

                for room_clients in rooms.values():
                    room_clients.discard(
                        client_socket
                    )


def load_rooms_from_database():
    """Load saved chat rooms into the server's in-memory room list."""
    database_rooms = get_rooms()

    with clients_lock:
        for room_name in database_rooms:
            if room_name not in rooms:
                rooms[room_name] = set()


def authenticate_client(client_socket):
    """Handle client authentication and return the logged-in username."""
    try:
        send_message(
            client_socket,
            "Enter your username:"
        )

        data = client_socket.recv(4096)

        if not data:
            return None

        message = data.decode("utf-8").strip()

        if message.startswith("/register "):
            parts = message.split(
                " ",
                2
            )

            if len(parts) != 3:
                send_message(
                    client_socket,
                    "Usage: /register username password"
                )
                return None

            username = parts[1].strip()
            password = parts[2]

            success, response = register_user(
                username,
                password
            )

            send_message(
                client_socket,
                response
            )

            return None

        if message.startswith("/login "):
            parts = message.split(
                " ",
                2
            )

            if len(parts) != 3:
                send_message(
                    client_socket,
                    "Usage: /login username password"
                )
                return None

            username = parts[1].strip()
            password = parts[2]

            success, response = login_user(
                username,
                password
            )

            if not success:
                send_message(
                    client_socket,
                    response
                )
                return None

            send_message(
                client_socket,
                "LOGIN_SUCCESS"
            )

            return username

        username = message

        if not username:
            username = "Guest"

        return username

    except (
        ConnectionResetError,
        ConnectionAbortedError,
        BrokenPipeError,
        OSError
    ):
        return None


def handle_client(client_socket, address):
    """Handle communication with a single connected client."""
    username = None
    current_room = "General"

    try:
        username = authenticate_client(
            client_socket
        )

        if not username:
            return

        with clients_lock:
            clients[client_socket] = {
                "username": username,
                "room": "General"
            }

            rooms["General"].add(
                client_socket
            )

        print(
            f"{username} connected from {address}"
        )

        join_message = (
            f"[{get_timestamp()}] "
            f"{username} joined General."
        )

        broadcast_to_room(
            "General",
            join_message,
            client_socket
        )

        while True:
            data = client_socket.recv(4096)

            if not data:
                break

            message = data.decode(
                "utf-8"
            ).strip()

            if not message:
                continue

            # Return the list of available rooms.
            if message == "/rooms":
                room_list = get_rooms()

                room_text = (
                    "Available rooms: "
                    + ", ".join(room_list)
                )

                send_message(
                    client_socket,
                    room_text
                )
                continue

            # Create a new chat room.
            if message.startswith("/create "):
                room_name = message[8:].strip()

                if db_create_room(room_name):
                    with clients_lock:
                        rooms.setdefault(
                            room_name,
                            set()
                        )

                    send_message(
                        client_socket,
                        (
                            f"Room '{room_name}' "
                            "created successfully."
                        )
                    )
                else:
                    send_message(
                        client_socket,
                        (
                            "Could not create room. "
                            "The room may already exist."
                        )
                    )

                continue

            # Move the client to another existing room.
            if message.startswith("/join "):
                room_name = message[6:].strip()

                if not room_exists(room_name):
                    send_message(
                        client_socket,
                        (
                            f"Room '{room_name}' "
                            "does not exist."
                        )
                    )
                    continue

                old_room = current_room

                with clients_lock:
                    rooms.setdefault(
                        room_name,
                        set()
                    )

                    rooms[old_room].discard(
                        client_socket
                    )

                    rooms[room_name].add(
                        client_socket
                    )

                    clients[client_socket]["room"] = (
                        room_name
                    )

                current_room = room_name

                if old_room != room_name:
                    leave_message = (
                        f"[{get_timestamp()}] "
                        f"{username} left {old_room}."
                    )

                    broadcast_to_room(
                        old_room,
                        leave_message,
                        client_socket
                    )

                send_message(
                    client_socket,
                    f"You joined room: {room_name}"
                )

                # Send the latest 50 saved messages to the user.
                history = get_message_history(
                    room_name,
                    limit=50
                )

                if history:
                    send_message(
                        client_socket,
                        "----- Message History -----"
                    )

                    for (
                        history_username,
                        history_message,
                        timestamp
                    ) in history:
                        formatted_history = (
                            f"[{timestamp}] "
                            f"{history_username}: "
                            f"{history_message}"
                        )

                        send_message(
                            client_socket,
                            formatted_history
                        )

                    send_message(
                        client_socket,
                        "----- End History -----"
                    )

                join_message = (
                    f"[{get_timestamp()}] "
                    f"{username} joined {room_name}."
                )

                broadcast_to_room(
                    room_name,
                    join_message,
                    client_socket
                )

                continue

            formatted_message = (
                f"[{get_timestamp()}] "
                f"{username}: {message}"
            )

            print(
                f"[{current_room}] "
                f"{formatted_message}"
            )

            # Save every chat message before broadcasting it.
            save_message(
                current_room,
                username,
                message
            )

            broadcast_to_room(
                current_room,
                formatted_message,
                client_socket
            )

    except (
        ConnectionResetError,
        ConnectionAbortedError,
        BrokenPipeError,
        OSError
    ):
        pass

    finally:
        # Remove the client from the server's active connections.
        with clients_lock:
            client_info = clients.pop(
                client_socket,
                None
            )

            for room_clients in rooms.values():
                room_clients.discard(
                    client_socket
                )

        try:
            client_socket.close()
        except OSError:
            pass

        if client_info:
            username = client_info["username"]
            room_name = client_info["room"]

            leave_message = (
                f"[{get_timestamp()}] "
                f"{username} left {room_name}."
            )

            print(leave_message)

            broadcast_to_room(
                room_name,
                leave_message
            )


def start_server():
    """Initialize the database and start accepting client connections."""
    initialize_database()
    load_rooms_from_database()

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server_socket.bind(
        (HOST, PORT)
    )

    server_socket.listen()

    print("Chat server started.")
    print(f"Listening on {HOST}:{PORT}")

    print(
        "Available rooms: "
        + ", ".join(get_rooms())
    )

    print("Waiting for clients...")

    try:
        while True:
            client_socket, address = (
                server_socket.accept()
            )

            # Handle each client independently.
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address),
                daemon=True
            )

            client_thread.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()