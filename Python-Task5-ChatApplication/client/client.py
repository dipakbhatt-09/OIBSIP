import socket
import threading


HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client_socket, stop_event):
    """Receive messages from the server in a background thread."""
    while not stop_event.is_set():
        try:
            message = client_socket.recv(4096).decode("utf-8")

            if not message:
                print("\nDisconnected from server.")
                stop_event.set()
                break

            print(f"\n{message}")
            print("You: ", end="", flush=True)

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            OSError
        ):
            if not stop_event.is_set():
                print("\nDisconnected from server.")

            stop_event.set()
            break


def start_client():
    """Connect to the chat server and start the CLI client."""
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Event used to safely stop the receiving thread.
    stop_event = threading.Event()
    receive_thread = None

    try:
        client_socket.connect((HOST, PORT))

        # The server first asks the client for a username.
        prompt = client_socket.recv(1024).decode("utf-8")
        print(prompt, end="")

        username = input().strip()

        if not username:
            print("Username cannot be empty.")
            return

        client_socket.send(username.encode("utf-8"))

        # Receive server messages without blocking the input loop.
        receive_thread = threading.Thread(
            target=receive_messages,
            args=(client_socket, stop_event)
        )

        receive_thread.start()

        print("Connected to chat server.")
        print("Type your message and press Enter.")
        print("Type /quit to leave.\n")

        while not stop_event.is_set():
            try:
                message = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if message == "/quit":
                break

            if not message:
                continue

            try:
                client_socket.send(message.encode("utf-8"))

            except (
                ConnectionResetError,
                BrokenPipeError,
                OSError
            ):
                print("Connection to server was lost.")
                break

    except ConnectionRefusedError:
        print("Could not connect to the server.")

    except (
        ConnectionResetError,
        ConnectionAbortedError,
        OSError
    ):
        print("Connection to the server was closed.")

    except (KeyboardInterrupt, EOFError):
        print("\nClient stopped.")

    finally:
        # Stop the receiver thread before closing the socket.
        stop_event.set()

        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        client_socket.close()

        if receive_thread is not None:
            receive_thread.join(timeout=1)

        print("Client closed.")


if __name__ == "__main__":
    start_client()
