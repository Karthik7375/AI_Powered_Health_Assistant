import streamlit as st
import requests
import sqlite3
from transformers import pipeline
from dotenv import load_dotenv
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')








# Database Connection
conn = sqlite3.connect("health_assistant.db", check_same_thread=False)
cursor = conn.cursor()






from groq import Groq
groq_api_key = "your_groq_api_key"
#os.getenv("GROQ_API_KEY")

def generate_response(user_input):
    
    
    # Check if the response is empty or not meaningful
    if not user_input or "I'm a health assistant"  in user_input:
        ai_response = "Please consult a healthcare professional."

    elif "medicine" in user_input:
        ai_response = ".Take your medicine regularly as the doctor prescibed"
        
    elif "appointment" in user_input:
        ai_response = ".Please visit the doctor's office immediately"
        
    elif "fever" in user_input.lower():
        return "If you have a fever, it's important to rest and stay hydrated. Over-the-counter medications like  (Tylenol) or (Advil) can help reduce fever."
    elif "back pain" in user_input.lower():
        return "For back pain, it's important to maintain good posture and avoid heavy lifting. Over-the-counter pain relievers like ibuprofen can help. If the pain persists, please consult a doctor."
    elif "headache" in user_input.lower():
        return "For headaches, staying hydrated and resting in a quiet, dark room can help.  pain relievers like acetaminophen or ibuprofen can also be effective. If headaches are frequent or severe, please consult a doctor."
    elif "cold" in user_input.lower():
        return "For a common cold, rest and stay hydrated. Medications can help relieve symptoms."
    else:
        client = Groq(api_key=groq_api_key)
        completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a health assistant, Provide information based on condition /"
                "and filter out confidential information. If anything non medical is asked. Politely refuse to answer and say that I am a medical chatbot"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
        )
        response = ""
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")
            response += chunk.choices[0].delta.content or ""        
            
        return response


def save_chat(username, question, answer):
    cursor.execute("INSERT INTO history (username, question, answer) VALUES (?, ?, ?)", (username, question, answer))
    conn.commit()

def get_chat_history(username):
    cursor.execute("SELECT question, answer FROM history WHERE username = ?", (username,))
    return cursor.fetchall()


import html
import re

def sanitize_input(user_input):
    # Remove any HTML tags
    sanitized_input = re.sub(r'<.*?>', '', user_input)
    # Escape HTML special characters
    sanitized_input = html.escape(sanitized_input)
    return sanitized_input

# Streamlit UI for Chatbot
def chatbot_ui():
    st.title("💬 AI Chatbot")
    st.sidebar.image("Logo.jpg",caption="Health Assistant")
    chat = st.sidebar.radio("Menu", ["Chatbot", "Chat History"])
    
    if chat == "Chatbot":
        user_input = st.text_area("Ask me anything about health:")
        if st.button("Get Advice"):
            user_input = sanitize_input(user_input=user_input)
            if user_input:
                with st.spinner("Thinking..."):
                    
                    ai_response = generate_response(user_input)  # Just pass the input directly
                    
                    
                    # Save Chat History
                    save_chat(st.session_state.username, user_input, ai_response)

                    # Display Response
                    st.write("💡 AI Response:", ai_response)
                    
    elif chat == "Chat History":
        # Show Previous Chat History
        st.subheader("📜 Your Chat History")
        history = get_chat_history(st.session_state.username)
        for question, answer in history:
            st.write(f"**Q:** {question}")
            st.write(f"**A:** {answer}")
            st.write("---")