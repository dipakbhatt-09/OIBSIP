import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# Window Setup
window = tk.Tk()
window.title("Random Password Generator")
window.geometry("560x720")
window.minsize(560, 680)
window.resizable(True, True)
window.configure(bg="#eef2f7")


# Colors
BG_COLOR = "#eef2f7"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#1f2937"
SECONDARY_TEXT = "#6b7280"
BUTTON_COLOR = "#2563eb"
PASSWORD_BG = "#f3f4f6"
HISTORY_BG = "#f9fafb"


# Variables
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
numbers_var = tk.BooleanVar()
symbols_var = tk.BooleanVar()
ambiguous_var = tk.BooleanVar()

password_history = []


# Main Card
main_frame = tk.Frame(
    window,
    bg=CARD_COLOR,
    padx=25,
    pady=10
)

main_frame.pack(
    padx=25,
    pady=25,
    fill="both",
    expand=True
)


# Header
title_label = tk.Label(
    main_frame,
    text="RANDOM PASSWORD GENERATOR",
    font=("Arial", 20, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

title_label.pack(pady=(0, 2))


subtitle_label = tk.Label(
    main_frame,
    text="Create a strong and secure password",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)

subtitle_label.pack(pady=(0, 8))



# Password Length
length_label = tk.Label(
    main_frame,
    text="Password Length",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

length_label.pack(anchor="w")


length_spinbox = tk.Spinbox(
    main_frame,
    from_=8,
    to=100,
    width=10,
    font=("Arial", 12),
    justify="center"
)

length_spinbox.pack(
    pady=(4, 8)
)


# Character Types
character_label = tk.Label(
    main_frame,
    text="Character Types",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

character_label.pack(
    anchor="w",
    pady=(0, 4)
)


character_frame = tk.Frame(
    main_frame,
    bg=CARD_COLOR
)

character_frame.pack(
    fill="x"
)


# Uppercase
uppercase_check = tk.Checkbutton(
    character_frame,
    text="Uppercase",
    variable=uppercase_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    activebackground=CARD_COLOR
)

uppercase_check.grid(
    row=0,
    column=0,
    sticky="w",
    padx=5
)


# Lowercase
lowercase_check = tk.Checkbutton(
    character_frame,
    text="Lowercase",
    variable=lowercase_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    activebackground=CARD_COLOR
)

lowercase_check.grid(
    row=0,
    column=1,
    sticky="w",
    padx=5
)


# Numbers
numbers_check = tk.Checkbutton(
    character_frame,
    text="Numbers",
    variable=numbers_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    activebackground=CARD_COLOR
)

numbers_check.grid(
    row=1,
    column=0,
    sticky="w",
    padx=5
)


# Symbols
symbols_check = tk.Checkbutton(
    character_frame,
    text="Symbols",
    variable=symbols_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    activebackground=CARD_COLOR
)

symbols_check.grid(
    row=1,
    column=1,
    sticky="w",
    padx=5
)



# Ambiguous Characters
ambiguous_check = tk.Checkbutton(
    main_frame,
    text="Exclude Ambiguous Characters (0, O, l, 1)",
    variable=ambiguous_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    activebackground=CARD_COLOR
)

ambiguous_check.pack(
    anchor="w",
    pady=(4, 7)
)



# Password Strength
def check_strength(password):

    score = 0

    # Check length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    # Check uppercase
    if any(char.isupper() for char in password):
        score += 1

    # Check lowercase
    if any(char.islower() for char in password):
        score += 1

    # Check numbers
    if any(char.isdigit() for char in password):
        score += 1

    # Check symbols
    if any(char in string.punctuation for char in password):
        score += 1

    # Return strength
    if score <= 2:
        return "Weak"

    elif score <= 4:
        return "Medium"

    else:
        return "Strong"



# Generate Password
def generate_password():

    # Get password length
    try:
        length = int(length_spinbox.get())

    except ValueError:
        messagebox.showerror(
            "Invalid Length",
            "Please enter a valid number."
        )
        return

    # Check minimum length
    if length < 8:
        messagebox.showerror(
            "Invalid Length",
            "Password length must be at least 8 characters."
        )
        return

    # Get selected character types
    character_sets = []

    if uppercase_var.get():
        character_sets.append(string.ascii_uppercase)

    if lowercase_var.get():
        character_sets.append(string.ascii_lowercase)

    if numbers_var.get():
        character_sets.append(string.digits)

    if symbols_var.get():
        character_sets.append(string.punctuation)

    # At least 2 types are required
    if len(character_sets) < 2:
        messagebox.showerror(
            "Character Types Required",
            "Please select at least 2 character types."
        )
        return

    # Remove ambiguous characters
    if ambiguous_var.get():

        ambiguous_characters = "0Ol1"

        character_sets = [
            "".join(
                char
                for char in character_set
                if char not in ambiguous_characters
            )
            for character_set in character_sets
        ]

    # Add one character from every selected type
    password_characters = []

    for character_set in character_sets:

        password_characters.append(
            secrets.choice(character_set)
        )

    # Combine all selected characters
    all_characters = "".join(character_sets)

    # Add remaining characters
    remaining_length = length - len(password_characters)

    for _ in range(remaining_length):

        password_characters.append(
            secrets.choice(all_characters)
        )

    # Securely shuffle password
    for i in range(len(password_characters) - 1, 0, -1):

        j = secrets.randbelow(i + 1)

        password_characters[i], password_characters[j] = (
            password_characters[j],
            password_characters[i]
        )

    password = "".join(password_characters)

    # Display password
    password_display.config(
        text=password
    )

    # Check password strength
    strength = check_strength(password)

    strength_label.config(
        text=f"Password Strength: {strength}"
    )

    # Update strength bar
    if strength == "Weak":

        strength_bar.config(
            width=80
        )

    elif strength == "Medium":

        strength_bar.config(
            width=170
        )

    else:

        strength_bar.config(
            width=260
        )

    # Copy password automatically
    pyperclip.copy(password)

    # Add password to history
    password_history.append(password)

    # Keep only last 5 passwords
    latest_passwords = password_history[-5:]

    # Clear history display
    history_text.delete(
        "1.0",
        tk.END
    )

    # Display latest passwords first
    for index, old_password in enumerate(
        reversed(latest_passwords),
        start=1
    ):

        history_text.insert(
            tk.END,
            f"{index}. {old_password}\n"
        )


# Generate Button
generate_button = tk.Button(
    main_frame,
    text="GENERATE PASSWORD",
    font=("Arial", 11, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    activebackground=BUTTON_COLOR,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=14,
    command=generate_password
)

generate_button.pack(
    fill="x",
    pady=(0, 8)
)


# Password Display
password_title = tk.Label(
    main_frame,
    text="Generated Password",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

password_title.pack(
    anchor="w"
)


password_display = tk.Label(
    main_frame,
    text="Your password will appear here",
    font=("Arial", 12, "bold"),
    bg=PASSWORD_BG,
    fg=TEXT_COLOR,
    padx=10,
    pady=12,
    wraplength=430
)

password_display.pack(
    fill="x",
    pady=(4, 6)
)


# Strength Indicator
strength_label = tk.Label(
    main_frame,
    text="Password Strength: -",
    font=("Arial", 10, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

strength_label.pack(
    pady=(0, 6)
)


strength_background = tk.Frame(
    main_frame,
    bg="#d1d5db",
    height=8
)

strength_background.pack(
    fill="x",
    pady=(0, 9)
)

strength_background.pack_propagate(False)


strength_bar = tk.Frame(
    strength_background,
    bg=BUTTON_COLOR,
    width=0,
    height=8
)

strength_bar.pack(
    side="left"
)


# Copy Button
def copy_password():

    password = password_display.cget("text")

    # Check if password exists
    if password == "Your password will appear here":

        messagebox.showwarning(
            "No Password",
            "Please generate a password first."
        )

        return

    # Copy password
    pyperclip.copy(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard!"
    )


copy_button = tk.Button(
    main_frame,
    text="COPY TO CLIPBOARD",
    font=("Arial", 10, "bold"),
    bg="#e5e7eb",
    fg=TEXT_COLOR,
    activebackground="#d1d5db",
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=11,
    command=copy_password
)

copy_button.pack(
    fill="x",
    pady=(0, 7)
)


# History
history_label = tk.Label(
    main_frame,
    text="Generation History (Last 5)",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

history_label.pack(
    anchor="w",
    pady=(0, 4)
)


history_text = tk.Text(
    main_frame,
    height=5,
    font=("Consolas", 10),
    bg=HISTORY_BG,
    fg=TEXT_COLOR,
    relief="solid",
    borderwidth=1,
    padx=8,
    pady=5
)

history_text.pack(
    fill="x"
)


# Start Application
window.mainloop()