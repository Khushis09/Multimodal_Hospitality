import streamlit as st
import speech_recognition as sr
import requests
import time
import urllib.parse

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Multimodal Hospitality Creator", layout="wide")

# ------------------ HIDE STREAMLIT UI ------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "cache" not in st.session_state:
    st.session_state.cache = {}

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ FAST API CALL ------------------
@st.cache_data(show_spinner=False)
def fetch_description(prompt):
    try:
        url = f"http://127.0.0.1:8000/generate?prompt={urllib.parse.quote(prompt)}"
        res = requests.get(url, timeout=20)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {
            "description": f"❌ Backend Error: {str(e)}",
            "image": None
        }

# ------------------ VOICE INPUT ------------------
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return ""

# ------------------ UI STYLING ------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: white;
}
.glass {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(20px);
}
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(45deg, #6366f1, #9333ea);
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("✨ Multimodal Hospitality Creator")

# ------------------ INPUT ------------------
prompt = st.text_input("Enter your idea")

if st.button("🎤 Speak"):
    spoken = voice_input()
    if spoken:
        prompt = spoken
        st.success(f"You said: {prompt}")

# ------------------ GENERATE ------------------
if st.button("Generate"):

    if not prompt:
        st.warning("Enter prompt")
        st.stop()

    # CACHE FIRST
    if prompt in st.session_state.cache:
        data = st.session_state.cache[prompt]
    else:
        data = fetch_description(prompt)
        st.session_state.cache[prompt] = data

    # FAST IMAGE (Pollinations)
    enhanced_prompt = f"luxury hotel {prompt} ultra realistic 4k cinematic"
    image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced_prompt)}"

    col1, col2 = st.columns(2)

    # ---------------- IMAGE ----------------
    with col1:
        st.markdown("### 🖼️ AI Design")

        st.image(image_url, use_container_width=True)

        try:
            img_bytes = requests.get(image_url, timeout=10).content
            st.download_button(
                "📥 Download",
                img_bytes,
                file_name="design.png",
                mime="image/png"
            )
        except:
            st.warning("Download failed")

    # ---------------- DESCRIPTION ----------------
    with col2:
        st.markdown("### 📝 Description")

        placeholder = st.empty()
        placeholder.markdown("⏳ Generating luxury experience...")

        time.sleep(0.3)

        placeholder.markdown(
            f"<div class='glass'>{data['description']}</div>",
            unsafe_allow_html=True
        )

    # SAVE HISTORY
    if prompt not in st.session_state.history:
        st.session_state.history.append(prompt)

# ------------------ HISTORY ------------------
st.markdown("### 🕒 History")
for item in st.session_state.history[::-1]:
    st.markdown(f"- {item}")