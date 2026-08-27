import secrets
import string


# Ask the user to choose the character types
def get_character_sets():

    print("\nChoose character types:")
    print("1. Uppercase letters")
    print("2. Lowercase letters")
    print("3. Numbers")
    print("4. Symbols")

    while True:
        choices = input("Enter your choices (e.g. 1234): ").strip()

        # Check if the user entered nothing
        if not choices:
            print("Please select at least 2 character types.")
            continue

        # Check for invalid choices
        if any(choice not in "1234" for choice in choices):
            print("Invalid choice. Please enter only 1, 2, 3, or 4.")
            continue

        # Remove duplicate choices
        choices = set(choices)

        # At least 2 character types are required
        if len(choices) < 2:
            print("Please select at least 2 character types.")
            continue

        break

    character_sets = []

    if "1" in choices:
        character_sets.append(string.ascii_uppercase)

    if "2" in choices:
        character_sets.append(string.ascii_lowercase)

    if "3" in choices:
        character_sets.append(string.digits)

    if "4" in choices:
        character_sets.append(string.punctuation)

    return character_sets


# Generate a secure random password
def generate_password(length, character_sets):

    # Add one character from each selected type
    password_characters = []

    for character_set in character_sets:
        password_characters.append(secrets.choice(character_set))

    # Combine all selected character types
    all_characters = "".join(character_sets)

    # Fill the remaining password length
    remaining_length = length - len(password_characters)

    for _ in range(remaining_length):
        password_characters.append(secrets.choice(all_characters))

    # Shuffle the password characters
    for i in range(len(password_characters) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_characters[i], password_characters[j] = (
            password_characters[j],
            password_characters[i]
        )

    return "".join(password_characters)


# Get the password length from the user
def get_password_length():

    while True:
        try:
            length = int(input("\nEnter password length (minimum 8): "))

            # Password must contain at least 8 characters
            if length < 8:
                print("Password length must be at least 8.")
                continue

            return length

        except ValueError:
            print("Please enter a valid number.")


# Check the password strength
def calculate_strength(length, character_sets):

    diversity = len(character_sets)

    if length >= 16 and diversity >= 4:
        return "Strong"

    if length >= 12 and diversity >= 3:
        return "Strong"

    if length >= 10 and diversity >= 2:
        return "Medium"

    return "Weak"


# Main program
def main():

    print("   RANDOM PASSWORD GENERATOR")

    while True:

        # Get password length
        length = get_password_length()

        # Get selected character types
        character_sets = get_character_sets()

        # Generate the password
        password = generate_password(
            length,
            character_sets
        )

        # Check password strength
        strength = calculate_strength(
            length,
            character_sets
        )

        print("Your password:", password)
        print("Password length:", length)
        print("Password strength:", strength)
      
        # Ask if the user wants another password
        again = input(
            "\nGenerate another password? (y/n): "
        ).strip().lower()

        if again != "y":
            print("\nThank you for using Password Generator!")
            break


# Start the program
if __name__ == "__main__":
    main()