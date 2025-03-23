import re
import random
import streamlit as st

# List of weak passwords (blacklist)
COMMON_WEAK_PASSWORDS = ["password", "123456", "qwerty", "password123", "abc123", "letmein", "admin", "welcome"]

SPECIAL_CHARACTERS = "!@#$%^&*"

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Check if password is in the blacklist
    if password.lower() in COMMON_WEAK_PASSWORDS:
        return "❌ Weak Password - This password is too common!", ["Avoid using easily guessable passwords like 'password123' or '123456'."]

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Strength Rating
    if score == 4:
        return "✅ Strong Password!", []
    elif score == 3:
        return "⚠️ Moderate Password - Consider adding more security features.", feedback
    else:
        return "❌ Weak Password - Improve it using the suggestions below.", feedback

# Function to generate a strong password
def generate_strong_password(length=12):
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    special = "!@#$%^&*"

    # Ensure at least one character from each category
    password = [
        random.choice(upper),
        random.choice(lower),
        random.choice(digits),
        random.choice(special)
    ]

    # Fill the rest randomly
    all_characters = upper + lower + digits + special
    password += random.choices(all_characters, k=length - 4)
    random.shuffle(password)
    
    return "".join(password)

# Streamlit UI
st.title("🔐 Password Strength Meter")

password = st.text_input("Enter your password:", type="password")

if password:
    strength_message, feedback = check_password_strength(password)
    st.write(strength_message)

    if feedback:
        st.write("\n💡 Suggestions:")
        for tip in feedback:
            st.write("- ", tip)

    if "Weak Password" in strength_message:
        st.write("\n🔑 Suggested Strong Password: ", generate_strong_password())
