import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="🏋️‍♂️ Fitness Query AI Chatbot", page_icon="🏋️‍♂️")
st.title("🏋️‍♂️ Fitness Query AI Chatbot")
st.write("Ask me anything about workouts, nutrition, and fitness! 💪")

# ✅ Load API key securely
API_KEY = st.secrets.get("GEMINI_API_KEY")
if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found in secrets.")
    st.stop()

# ✅ Configure Gemini
genai.configure(api_key=API_KEY)

# ✅ Custom system instruction
system_instruction = (
    "You are a friendly, knowledgeable fitness assistant. "
    "You provide clear, practical, and accurate answers to user questions about exercise, "
    "workouts, nutrition, recovery, and general fitness advice. "
    "Always keep your responses supportive, concise, and easy to understand. "
    "If a question is outside your scope (like medical diagnosis), politely suggest that the user consult "
    "a qualified healthcare professional. Be encouraging and motivate users to pursue healthy, safe fitness habits."
)

# ✅ Initialize chat with system prompt
if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",  # fallback to "gemini-1.5-flash" if needed
        system_instruction=system_instruction
    )
    st.session_state.chat = model.start_chat(history=[])

# ✅ Display previous chat history
for msg in st.session_state.chat.history:
    with st.chat_message("user" if msg.role == "user" else "assistant"):
        st.markdown(msg.parts[0].text if msg.parts else msg.text)

# ✅ Accept and process user input
if prompt := st.chat_input("Type your fitness question here..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error("⚠️ Could not generate a response. Check your API key or model access.")