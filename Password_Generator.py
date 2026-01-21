import streamlit as st
import random
import string

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    characters = ""

    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return ""

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


st.set_page_config(page_title="Password Generator", page_icon="🔐")

st.title("🔐 Password Generator")

length = st.slider("Password Length", min_value=4, max_value=32, value=12)

use_upper = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
use_lower = st.checkbox("Include Lowercase Letters (a-z)", value=True)
use_digits = st.checkbox("Include Numbers (0-9)", value=True)
use_symbols = st.checkbox("Include Special Characters (!@#$)", value=True)

if st.button("Generate Password"):
    password = generate_password(
        length,
        use_upper,
        use_lower,
        use_digits,
        use_symbols
    )

    if password:
        st.success("Your Generated Password:")
        st.code(password)
    else:
        st.error("Please select at least one character type.")
      
