import random
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    if length < 1:
        return "Password length must be at least 1"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def password_strength_feedback(password):
    if len(password) < 8:
        return "Weak password: Consider making it longer."
    elif len(password) < 12:
        return "Moderate password: Good, but could be stronger."
    else:
        return "Strong password."

length = int(input("Enter the desired password length: "))
generated_password = generate_password(length)

print("Generated Password:", generated_password)

print(password_strength_feedback(generated_password))
