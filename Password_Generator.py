import streamlit as st
import random
import string

def generate_password(length, characters):
    return ''.join(random.choice(characters) for _ in range(length))


st.set_page_config(page_title="Password Generator", page_icon="🔐")
st.title("🔐 Password Generator")

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Password length
length = st.slider(
    "Password Length",
    min_value=4,
    max_value=100,
    value=12
)

# Number of passwords
count = st.number_input(
    "How many passwords do you want?",
    min_value=1,
    max_value=50,
    value=5
)

# Character options
use_upper = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
use_lower = st.checkbox("Include Lowercase Letters (a-z)", value=True)
use_digits = st.checkbox("Include Numbers (0-9)", value=True)
use_symbols = st.checkbox("Include Special Characters (!@#$)", value=True)

if st.button("Generate Passwords"):
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
        st.error("❌ Please select at least one character type.")
    else:
        st.success("✅ Generated Passwords:")
        for _ in range(count):
            password = generate_password(length, characters)
            st.code(password)
            st.session_state.history.append(password)

# Show history
st.divider()
st.subheader("📜 Password History")

if st.session_state.history:
    for i, pwd in enumerate(st.session_state.history, start=1):
        st.text(f"{i}. {pwd}")
else:
    st.info("No passwords generated yet.")

# Clear history button
if st.button("🗑️ Clear History"):
    st.session_state.history.clear()
    st.success("History cleared!")
    
