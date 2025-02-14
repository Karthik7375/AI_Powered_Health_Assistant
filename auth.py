import streamlit as st
import sqlite3
import hashlib

# Database Connection
conn = sqlite3.connect("health_assistant.db", check_same_thread=False)
cursor = conn.cursor()


cursor = conn.cursor()

# Create Tables. This has to be done only once as once the table is created

cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    FOREIGN KEY (username) REFERENCES accounts(username))''')


conn.commit()


# Helper Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    hashed_pw = hash_password(password)
    cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", (username, hashed_pw))
    return cursor.fetchone() is not None

# Streamlit UI for Authentication
def auth_ui():
    st.title("🩺 AI-Powered Health Assistant - Login/Register")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    st.sidebar.image("Logo.jpg",caption="Health Assistant")
    menu = st.sidebar.radio("Menu", ["Login", "Register"])

    if menu == "Register":
        st.subheader("Create a New Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created! You can log in now.")
            else:
                st.error("Username already exists!")

    elif menu == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password")