import socket
import threading
import tkinter as tk
from tkinter import messagebox

from emoji import replace_emojis


HOST = "127.0.0.1"
PORT = 5000

# Application colors
BG = "#f4f7fb"
BLUE = "#2563eb"
DARK_BLUE = "#1e40af"
LIGHT_BLUE = "#eaf2ff"
WHITE = "#ffffff"
TEXT = "#1f2937"
GRAY = "#6b7280"
BORDER = "#dbe3ef"


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("900x600")
        self.root.minsize(750, 500)
        self.root.configure(bg=BG)

        # Connection state
        self.client_socket = None
        self.receive_thread = None
        self.receive_buffer = ""
        self.connected = False
        self.disconnecting = False

        # User and room state
        self.current_room = "General"
        self.username = ""

        # Used for message notifications
        self.window_focused = True

        self.show_login_screen()

        self.root.bind(
            "<FocusIn>",
            self.on_focus_in
        )
        self.root.bind(
            "<FocusOut>",
            self.on_focus_out
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    def clear_window(self):
        """Remove all widgets from the main window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_button(self, parent, text, command, width=None):
        """Create a standard application button."""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=7
        )

        if width:
            button.config(width=width)

        return button

    # Login and registration

    def show_login_screen(self):
        """Display the login and registration screen."""
        self.clear_window()

        self.root.title(
            "Chat Application - Login"
        )

        outer = tk.Frame(
            self.root,
            bg=BG
        )
        outer.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            outer,
            bg=WHITE,
            bd=1,
            relief="solid"
        )
        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=430,
            height=430
        )

        title = tk.Label(
            card,
            text="Chat Application",
            bg=WHITE,
            fg=BLUE,
            font=("Arial", 24, "bold")
        )
        title.pack(
            pady=(40, 5)
        )

        subtitle = tk.Label(
            card,
            text="Login to continue chatting",
            bg=WHITE,
            fg=GRAY,
            font=("Arial", 10)
        )
        subtitle.pack(
            pady=(0, 30)
        )

        username_label = tk.Label(
            card,
            text="Username",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 10, "bold")
        )
        username_label.pack(
            anchor="w",
            padx=55
        )

        self.username_entry = tk.Entry(
            card,
            font=("Arial", 11),
            bd=1,
            relief="solid"
        )
        self.username_entry.pack(
            fill="x",
            padx=55,
            pady=(6, 18),
            ipady=6
        )

        password_label = tk.Label(
            card,
            text="Password",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 10, "bold")
        )
        password_label.pack(
            anchor="w",
            padx=55
        )

        self.password_entry = tk.Entry(
            card,
            show="*",
            font=("Arial", 11),
            bd=1,
            relief="solid"
        )
        self.password_entry.pack(
            fill="x",
            padx=55,
            pady=(6, 25),
            ipady=6
        )

        button_frame = tk.Frame(
            card,
            bg=WHITE
        )
        button_frame.pack()

        login_button = self.create_button(
            button_frame,
            "Login",
            self.login,
            12
        )
        login_button.pack(
            side="left",
            padx=5
        )

        register_button = tk.Button(
            button_frame,
            text="Register",
            command=self.register,
            bg=LIGHT_BLUE,
            fg=BLUE,
            activebackground="#dbeafe",
            activeforeground=DARK_BLUE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Arial", 10, "bold"),
            width=12,
            padx=10,
            pady=7
        )
        register_button.pack(
            side="left",
            padx=5
        )

        self.status_label = tk.Label(
            card,
            text="",
            bg=WHITE,
            fg=GRAY,
            font=("Arial", 9)
        )
        self.status_label.pack(
            pady=20
        )

        self.username_entry.focus_force()

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

    def connect_for_auth(self):
        """Create a socket connection for authentication."""
        try:
            client_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            client_socket.connect(
                (HOST, PORT)
            )

            prompt = client_socket.recv(
                1024
            ).decode(
                "utf-8"
            ).strip()

            if not prompt:
                client_socket.close()
                return None

            return client_socket

        except (
            ConnectionRefusedError,
            ConnectionResetError,
            OSError
        ):
            messagebox.showerror(
                "Connection Error",
                "Could not connect to the chat server.\n\n"
                "Make sure the server is running."
            )

            return None

    def register(self):
        """Register a new user account."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )
            return

        client_socket = self.connect_for_auth()

        if client_socket is None:
            return

        try:
            command = f"/register {username} {password}"

            client_socket.sendall(
                command.encode("utf-8")
            )

            response = client_socket.recv(
                4096
            ).decode(
                "utf-8"
            ).strip()

            client_socket.close()

            if response == "Registration successful.":
                messagebox.showinfo(
                    "Registration",
                    "Registration successful.\n"
                    "You can now login."
                )

                self.password_entry.delete(
                    0,
                    tk.END
                )
            else:
                messagebox.showerror(
                    "Registration",
                    response
                )

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            BrokenPipeError,
            OSError
        ):
            client_socket.close()

            messagebox.showerror(
                "Error",
                "Connection to server was lost."
            )

    def login(self):
        """Authenticate the user and start the chat session."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )
            return

        client_socket = self.connect_for_auth()

        if client_socket is None:
            return

        try:
            command = f"/login {username} {password}"

            client_socket.sendall(
                command.encode("utf-8")
            )

            response = client_socket.recv(
                4096
            ).decode(
                "utf-8"
            ).strip()

            if response != "LOGIN_SUCCESS":
                client_socket.close()

                messagebox.showerror(
                    "Login Failed",
                    response
                )

                return

            self.client_socket = client_socket
            self.username = username
            self.connected = True
            self.disconnecting = False
            self.receive_buffer = ""

            self.show_chat_screen()

            self.receive_thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )

            self.receive_thread.start()

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            BrokenPipeError,
            OSError
        ):
            client_socket.close()

            messagebox.showerror(
                "Login Error",
                "Connection to server was lost."
            )

    # Chat interface

    def show_chat_screen(self):
        """Display the main chat interface."""
        self.clear_window()

        self.root.title(
            f"Chat Application - {self.username}"
        )

        main_frame = tk.Frame(
            self.root,
            bg=BG
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        self.build_room_sidebar(main_frame)
        self.build_chat_area(main_frame)

    def build_room_sidebar(self, parent):
        """Build the room list and room controls."""
        sidebar = tk.Frame(
            parent,
            bg=WHITE,
            width=210,
            bd=1,
            relief="solid"
        )
        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        logo = tk.Label(
            sidebar,
            text="CHAT ROOMS",
            bg=WHITE,
            fg=BLUE,
            font=("Arial", 14, "bold")
        )
        logo.pack(
            pady=(20, 5)
        )

        user_label = tk.Label(
            sidebar,
            text=f"Logged in as\n{self.username}",
            bg=WHITE,
            fg=GRAY,
            font=("Arial", 9)
        )
        user_label.pack(
            pady=(0, 15)
        )

        separator = tk.Frame(
            sidebar,
            bg=BORDER,
            height=1
        )
        separator.pack(
            fill="x",
            padx=15
        )

        room_label = tk.Label(
            sidebar,
            text="Available Rooms",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 10, "bold")
        )
        room_label.pack(
            anchor="w",
            padx=15,
            pady=(15, 8)
        )

        list_frame = tk.Frame(
            sidebar,
            bg=WHITE
        )
        list_frame.pack(
            fill="both",
            expand=True,
            padx=10
        )

        self.room_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 10),
            bg=LIGHT_BLUE,
            fg=TEXT,
            selectbackground=BLUE,
            selectforeground=WHITE,
            bd=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.room_listbox.pack(
            fill="both",
            expand=True
        )

        self.room_listbox.bind(
            "<Double-Button-1>",
            lambda event: self.join_selected_room()
        )

        create_button = self.create_button(
            sidebar,
            "+ Create Room",
            self.create_room
        )
        create_button.pack(
            fill="x",
            padx=15,
            pady=(12, 5)
        )

        join_button = self.create_button(
            sidebar,
            "Join Room",
            self.join_selected_room
        )
        join_button.pack(
            fill="x",
            padx=15,
            pady=5
        )

        refresh_button = tk.Button(
            sidebar,
            text="Refresh Rooms",
            command=self.request_rooms,
            bg=LIGHT_BLUE,
            fg=BLUE,
            activebackground="#dbeafe",
            activeforeground=DARK_BLUE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Arial", 9, "bold"),
            pady=6
        )
        refresh_button.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.current_room_label = tk.Label(
            sidebar,
            text="Room: General",
            bg=WHITE,
            fg=BLUE,
            font=("Arial", 10, "bold")
        )
        self.current_room_label.pack(
            pady=12
        )

        logout_button = tk.Button(
            sidebar,
            text="Logout",
            command=self.logout,
            bg="#fee2e2",
            fg="#dc2626",
            activebackground="#fecaca",
            activeforeground="#b91c1c",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Arial", 9, "bold"),
            pady=6
        )
        logout_button.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

    def build_chat_area(self, parent):
        """Build the chat area and message input."""
        chat_frame = tk.Frame(
            parent,
            bg=BG
        )
        chat_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        header = tk.Frame(
            chat_frame,
            bg=BLUE,
            height=65
        )
        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        self.chat_title = tk.Label(
            header,
            text="General",
            bg=BLUE,
            fg=WHITE,
            font=("Arial", 16, "bold")
        )
        self.chat_title.pack(
            side="left",
            padx=20,
            pady=15
        )

        self.online_label = tk.Label(
            header,
            text="● Connected",
            bg=BLUE,
            fg="#dbeafe",
            font=("Arial", 9)
        )
        self.online_label.pack(
            side="right",
            padx=20
        )

        text_frame = tk.Frame(
            chat_frame,
            bg=BG
        )
        text_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.chat_area = tk.Text(
            text_frame,
            wrap="word",
            state="disabled",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            padx=12,
            pady=10,
            highlightthickness=0
        )
        self.chat_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            text_frame,
            command=self.chat_area.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.chat_area.config(
            yscrollcommand=scrollbar.set
        )

        bottom_frame = tk.Frame(
            chat_frame,
            bg=BG
        )
        bottom_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        self.message_entry = tk.Entry(
            bottom_frame,
            font=("Arial", 11),
            bg=WHITE,
            fg=TEXT,
            bd=1,
            relief="solid"
        )
        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8),
            ipady=7
        )

        send_button = self.create_button(
            bottom_frame,
            "Send",
            self.send_message,
            10
        )
        send_button.pack(
            side="right"
        )

        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        self.message_entry.focus_force()

        self.request_rooms()

    # Server communication

    def receive_messages(self):
        """Receive messages from the server in a background thread."""
        while self.connected and not self.disconnecting:
            try:
                data = self.client_socket.recv(
                    4096
                )

                if not data:
                    break

                self.receive_buffer += data.decode(
                    "utf-8"
                )

                # Process complete newline-delimited messages.
                while "\n" in self.receive_buffer:
                    message, self.receive_buffer = (
                        self.receive_buffer.split(
                            "\n",
                            1
                        )
                    )

                    message = message.strip()

                    if message:
                        self.root.after(
                            0,
                            self.handle_server_message,
                            message
                        )

            except (
                ConnectionResetError,
                ConnectionAbortedError,
                BrokenPipeError,
                OSError
            ):
                break

        if self.connected and not self.disconnecting:
            self.root.after(
                0,
                self.handle_server_disconnect
            )

    def handle_server_message(self, message):
        """Handle messages and server commands."""
        if message.startswith("Available rooms:"):
            room_text = message.replace(
                "Available rooms:",
                "",
                1
            ).strip()

            rooms = [
                room.strip()
                for room in room_text.split(",")
                if room.strip()
            ]

            self.room_listbox.delete(
                0,
                tk.END
            )

            for room in rooms:
                self.room_listbox.insert(
                    tk.END,
                    room
                )

            return

        if message.startswith("Room '"):
            self.add_chat_message(message)
            return

        if message.startswith(
            "Could not create room"
        ):
            self.add_chat_message(message)
            return

        if message.startswith("You joined room:"):
            room_name = message.split(
                ":",
                1
            )[1].strip()

            self.current_room = room_name

            self.current_room_label.config(
                text=f"Room: {room_name}"
            )

            self.chat_title.config(
                text=room_name
            )

            self.clear_chat_area()

            self.add_chat_message(message)

            return

        if message == "----- Message History -----":
            self.add_chat_message(message)
            return

        if message == "----- End History -----":
            self.add_chat_message(message)
            return

        self.add_chat_message(message)

        if not self.window_focused:
            self.show_notification()

    def show_notification(self):
        """Notify the user when a message arrives while unfocused."""
        self.root.bell()
        self.root.title(
            "🔔 New Message - Chat Application"
        )

    def add_chat_message(self, message):
        """Add a message to the chat display."""
        self.chat_area.config(
            state="normal"
        )

        self.chat_area.insert(
            tk.END,
            message + "\n"
        )

        self.chat_area.see(
            tk.END
        )

        self.chat_area.config(
            state="disabled"
        )

    def clear_chat_area(self):
        """Clear all messages from the chat display."""
        self.chat_area.config(
            state="normal"
        )

        self.chat_area.delete(
            "1.0",
            tk.END
        )

        self.chat_area.config(
            state="disabled"
        )

    def request_rooms(self):
        """Request the available rooms from the server."""
        if not self.connected:
            return

        try:
            self.client_socket.sendall(
                b"/rooms"
            )

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            BrokenPipeError,
            OSError
        ):
            self.handle_server_disconnect()

    def create_room(self):
        """Create a new chat room."""
        if not self.connected:
            return

        room_name = self.simple_input_dialog(
            "Create Room",
            "Enter new room name:"
        )

        if not room_name:
            return

        room_name = room_name.strip()

        if not room_name:
            return

        try:
            command = f"/create {room_name}"

            self.client_socket.sendall(
                command.encode("utf-8")
            )

            self.root.after(
                300,
                self.request_rooms
            )

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            BrokenPipeError,
            OSError
        ):
            self.handle_server_disconnect()

    def join_selected_room(self):
        """Join the selected chat room."""
        if not self.connected:
            return

        selection = self.room_listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "Join Room",
                "Please select a room first."
            )
            return

        room_name = self.room_listbox.get(
            selection[0]
        )

        try:
            command = f"/join {room_name}"

            self.client_socket.sendall(
                command.encode("utf-8")
            )

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            BrokenPipeError,
            OSError
        ):
            self.handle_server_disconnect()

    def send_message(self):
        """Send a message to the current room."""
        if not self.connected:
            return

        message = self.message_entry.get().strip()

        if not message:
            return

        # Convert supported shortcodes into Unicode emoji.
        message = replace_emojis(message)

        try:
            self.client_socket.sendall(
                message.encode("utf-8")
            )

            self.message_entry.delete(
                0,
                tk.END
            )

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            BrokenPipeError,
            OSError
        ):
            self.handle_server_disconnect()

    # Connection management

    def handle_server_disconnect(self):
        """Handle an unexpected server disconnection."""
        if self.disconnecting:
            return

        self.connected = False

        try:
            if self.client_socket:
                self.client_socket.close()
        except OSError:
            pass

        self.client_socket = None

        messagebox.showwarning(
            "Disconnected",
            "Connection to the chat server was lost."
        )

        self.show_login_screen()

    def logout(self):
        """Log out and return to the login screen."""
        if not self.connected:
            return

        self.disconnecting = True
        self.connected = False

        try:
            if self.client_socket:
                self.client_socket.shutdown(
                    socket.SHUT_RDWR
                )
        except OSError:
            pass

        try:
            if self.client_socket:
                self.client_socket.close()
        except OSError:
            pass

        self.client_socket = None
        self.receive_buffer = ""
        self.username = ""
        self.current_room = "General"

        self.show_login_screen()

    def on_close(self):
        """Close the connection and exit the application."""
        self.disconnecting = True
        self.connected = False

        try:
            if self.client_socket:
                self.client_socket.shutdown(
                    socket.SHUT_RDWR
                )
        except OSError:
            pass

        try:
            if self.client_socket:
                self.client_socket.close()
        except OSError:
            pass

        self.client_socket = None

        self.root.destroy()

    # Room creation dialog

    def simple_input_dialog(self, title, prompt):
        """Display a dialog for entering a room name."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("350x170")
        dialog.resizable(False, False)
        dialog.configure(bg=WHITE)

        dialog.transient(self.root)
        dialog.grab_set()

        label = tk.Label(
            dialog,
            text=prompt,
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 11, "bold")
        )
        label.pack(
            pady=(25, 10)
        )

        entry = tk.Entry(
            dialog,
            width=30,
            font=("Arial", 11),
            bd=1,
            relief="solid"
        )
        entry.pack(
            ipady=5
        )

        result = {
            "value": None
        }

        def submit():
            result["value"] = entry.get()
            dialog.destroy()

        def cancel():
            dialog.destroy()

        button_frame = tk.Frame(
            dialog,
            bg=WHITE
        )
        button_frame.pack(
            pady=18
        )

        create_button = self.create_button(
            button_frame,
            "Create",
            submit,
            10
        )
        create_button.pack(
            side="left",
            padx=5
        )

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=cancel,
            bg="#e5e7eb",
            fg=TEXT,
            activebackground="#d1d5db",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Arial", 9, "bold"),
            width=10,
            pady=7
        )
        cancel_button.pack(
            side="left",
            padx=5
        )

        entry.focus_force()

        entry.bind(
            "<Return>",
            lambda event: submit()
        )

        dialog.wait_window()

        return result["value"]

    # Window focus and notifications

    def on_focus_in(self, event=None):
        """Reset the notification title when focused."""
        self.window_focused = True

        if self.connected:
            self.root.title(
                f"Chat Application - {self.username}"
            )
        else:
            self.root.title(
                "Chat Application - Login"
            )

    def on_focus_out(self, event=None):
        """Track when the application loses focus."""
        self.window_focused = False


if __name__ == "__main__":
    root = tk.Tk()

    app = ChatApp(root)

    root.mainloop()