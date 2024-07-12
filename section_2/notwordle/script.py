from pwn import *
import string
import time

def check_password(guess):
    p = process('./notwordle')
    p.sendline(guess)
    output = p.recvuntil("characters match").decode('utf-8')
    print(output)
    
    # Extract the two digits at the specified positions
    try:
        correct_chars = int(output[83:85])  # Get characters at index 83 and 84 and convert to int
    except ValueError:
        print("Could not parse the number of correct characters.")
        correct_chars = None
        
    p.close()
    return correct_chars

# Possible characters (alphanumeric + '_')
possible_characters = string.ascii_letters + string.digits + '_'

# Initialize variables
password_length = 30
current_guess = ['.'] * password_length  # Start with all '_'
# Function to guess password
def guess_password():
    to_check = 1
    for i in range(password_length):
        for char in possible_characters:
            current_guess[i] = char
            guess = ''.join(current_guess)
            correct_count = check_password(guess)
            print(f"Trying '{guess}'... {correct_count} correct characters")
              # Pause for 1 second between guesses
            if int(correct_count) == to_check:
                to_check +=1
                break  # Move to the next character position
        print(f"Character '{current_guess[i]}' confirmed at position {i + 1}")
        time.sleep(1)

# Run the guessing function
guess_password()

# Print the final guessed password
final_guess = ''.join(current_guess)
print(f"Guessed password: {final_guess}")

# To get the final flag format
print(f"Flag: flag{{{final_guess}}}")
