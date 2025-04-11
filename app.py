import streamlit as st
from auth import auth_ui
from chatbot import chatbot_ui

def main():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        auth_ui()
    else:
        chatbot_ui()

if __name__ == "__main__":
    main()
    
    
"""
----------------SECURE CODING PRACTICES IMPLEMENTED----------------------------

1) AUTHENTICATION - sqlite with cookies
2) LOGGING AN APPLICATION - (Logging the Chat history) (Additionally needed whenever what user logged in -> to implement)

3) Input validation and sanitization - for log in,registration and llm chatbot input
4) Secure Password Storage - By Hashing the password
5) Parametrized Queries when inserting into DB - To avoid sql injection attacks
6) Session Management
7) Password Strength Check
--------------------------------------------------------------------------------- 
"""

