import streamlit as st
import sqlite3
import hashlib
import string
# Database Connection



import logging
# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)



conn = sqlite3.connect("health_assistant.db", check_same_thread=False)
cursor = conn.cursor()


cursor = conn.cursor()

# Create Tables. This has to be done only once as once the table is created, It is not needed

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

#Secure Coding Practices - Hashing Password (Authentication)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if login_user(username,password):
        return "User Already Exists"
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        logging.info(f"User  registered: {username}")
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    hashed_pw = hash_password(password)
    cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", (username, hashed_pw))
    if cursor.fetchone() is not None:
        logging.info(f"User  logged in: {username}")
    else:
        logging.warning(f"Registration attempt failed: {username} already exists.")

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
        
        
        # Input for password length
        length = st.number_input("Enter the desired password length:", min_value=1, max_value=100, value=12)

        # Button to generate password
        if st.button("Generate Password"):
            password = generate_password(length)
            st.success(f"Generated Password: {password}")
            
            
        if st.button("Register"):
            if input_validation(new_user,new_pass):
                if register_user(new_user, new_pass):
                    st.success("Account created! You can log in now.")
                else:
                    st.error("Username already exists!")
            else:
                st.error("Given input is invalid.Pls try again")

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



def input_validation(user,passw):
    if len(user) > 50:
        return st.error("Password is too long")
    
    else:
        user = user.strip('<>')
        
  
def password_checker(password):
    pass

def password_generator(length):
    
    import random
    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    numbers =  "0123456789"
    special_chr = "%$#@"
    
    new_password = ""
    
    length_of_possibile_characters = alphabets + numbers + special_chr
    for i in range(0,length):
        randomnumber = random.randint(0,length_of_possibile_characters)
        new_password += length_of_possibile_characters[randomnumber]

    return new_password


def generate_password(length):
    import random
    # Define the characters to use for the password
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate a random password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


