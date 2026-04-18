import streamlit as st
import speech_recognition as sr
import requests

st.set_page_config(page_title="Multimodal Hospitality Creator", layout="wide")

# Background
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.glass {
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
}
            .stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.stButton>button {
    border-radius: 12px;
    background: linear-gradient(45deg, #3b82f6, #9333ea);
    color: white;
    padding: 10px 20px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.title("✨ Multimodal Hospitality Creator")

# Prompt Input
prompt = st.text_input("Enter your idea")

# Voice Input
if st.button("🎤 Speak"):
    spoken = voice_input()
    if spoken:
        prompt = spoken
        st.success(f"You said: {prompt}")
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 बोलो...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except:
        return ""

if "history" not in st.session_state:
    st.session_state.history = []

# Generate
if st.button("Generate"):

    with st.spinner("Generating AI magic..."):
        try:
            res = requests.get(f"http://127.0.0.1:8000/generate?prompt={prompt}")
            data = res.json()

            st.session_state.history.append(prompt)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📄 Description")
                st.markdown(f"<div class='glass'>{data['description']}</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("### 🖼️ Image")
                if data["image"]:
                    st.image(data["image"])

                    st.download_button(
                        "Download Image",
                        requests.get(data["image"]).content,
                        file_name="design.png"
                    )

        except:
            st.error("Backend not running")

# History
st.markdown("### 🕒 History")
for item in st.session_state.history[::-1]:
    st.markdown(f"- {item}")

