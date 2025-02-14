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

load_dotenv()  # Load environment variables from .env file
HF_API_KEY = os.getenv("HF_API_KEY")




# Database Connection
conn = sqlite3.connect("health_assistant.db", check_same_thread=False)
cursor = conn.cursor()



# Load model directly
# Use a pipeline as a high-level helper
from transformers import pipeline

chatbot = pipeline("text-generation", model="microsoft/BioGPT-Large")

HF_API_KEY = os.getenv("HF_API_KEY")  # Ensure your API key is set



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
        response = chatbot(user_input, max_length=50, num_return_sequences=1)
        generated_text = response[0]['generated_text']
        if "fever" in generated_text.lower() or "symptom" in generated_text.lower():
            return generated_text
        else:
            return "Please consult a healthcare professional"
        
    
    return response


def save_chat(username, question, answer):
    cursor.execute("INSERT INTO history (username, question, answer) VALUES (?, ?, ?)", (username, question, answer))
    conn.commit()

def get_chat_history(username):
    cursor.execute("SELECT question, answer FROM history WHERE username = ?", (username,))
    return cursor.fetchall()

# Streamlit UI for Chatbot
def chatbot_ui():
    st.title("💬 AI Chatbot")
    st.sidebar.image("Logo.jpg",caption="Health Assistant")
    chat = st.sidebar.radio("Menu", ["Chatbot", "Chat History"])
    
    if chat == "Chatbot":
        user_input = st.text_area("Ask me anything about health:")
        if st.button("Get Advice"):
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