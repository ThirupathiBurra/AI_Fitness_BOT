import streamlit as st
import requests

# ---------------------------
# CONFIG
# ---------------------------
OPENROUTER_API_KEY = st.secrets["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"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

st.set_page_config(page_title="Fitness Query AI Chatbot", page_icon="🏋️‍♂️")
st.title("🏋️‍♂️ Fitness Query AI Chatbot")
st.write("Ask me anything about workouts, nutrition, and fitness! 💪")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly, knowledgeable fitness assistant. "
                "You provide clear, practical, and accurate answers to user questions about exercise, "
                "workouts, nutrition, recovery, and general fitness advice. "
                "Always keep your responses supportive, concise, and easy to understand. "
                "If a question is outside your scope (like medical diagnosis), politely suggest that the user consult "
                "a qualified healthcare professional. Be encouraging and motivate users to pursue healthy, safe fitness habits."
            )
        }
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# User input
prompt = st.chat_input("Type your fitness question here...")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare payload
    payload = {
        "model": MODEL_NAME,
        "messages": st.session_state.messages
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Call OpenRouter API
    with st.spinner("Thinking..."):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                assistant_message = data["choices"][0]["message"]["content"].strip()
            else:
                assistant_message = f"Oops! Something went wrong. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            assistant_message = f"Request failed: {e}"
        except ValueError:
            assistant_message = "Received invalid JSON from the API."

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    # Display assistant message
    st.chat_message("assistant").write(assistant_message)
