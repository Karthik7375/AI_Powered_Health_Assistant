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