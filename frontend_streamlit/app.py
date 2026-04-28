import streamlit as st
import speech_recognition as sr
import requests
import time
import urllib.parse
import logging

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Multimodal Hospitality Creator", layout="wide")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

if "show_generated_image" not in st.session_state:
    st.session_state.show_generated_image = False

if "generated_image_bytes" not in st.session_state:
    st.session_state.generated_image_bytes = None

if "debug_logs" not in st.session_state:
    st.session_state.debug_logs = []


def add_debug_log(message):
    timestamp = time.strftime("%H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    st.session_state.debug_logs.append(log_line)
    logger.info(message)


def fetch_image_bytes_with_retry(image_url, retries=3, timeout=20):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            add_debug_log(f"Fetching image (attempt {attempt}/{retries})")
            image_response = requests.get(image_url, timeout=timeout)
            add_debug_log(f"Image response status: {image_response.status_code}")
            image_response.raise_for_status()
            return image_response.content
        except Exception as e:
            last_error = e
            add_debug_log(f"Image fetch attempt {attempt} failed: {str(e)}")
            time.sleep(0.5 * attempt)

    raise RuntimeError(f"Image fetch failed after {retries} attempts: {str(last_error)}")

# ------------------ FAST API CALL ------------------
@st.cache_data(show_spinner=False)
def fetch_description(prompt):
    try:
        url = f"http://127.0.0.1:8000/generate?prompt={urllib.parse.quote(prompt)}"
        add_debug_log(f"Calling backend /generate for prompt: {prompt}")
        res = requests.get(url, timeout=20)
        add_debug_log(f"Backend response status: {res.status_code}")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        add_debug_log(f"Backend call failed: {str(e)}")
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

# ------------------ GENERATE ------------------
if st.button("Generate"):

    prompt = prompt.strip()

    if not prompt:
        st.warning("Enter prompt")
        st.stop()

    # CACHE FIRST
    if prompt in st.session_state.cache:
        add_debug_log(f"Cache hit for prompt: {prompt}")
        data = st.session_state.cache[prompt]
    else:
        add_debug_log(f"Cache miss for prompt: {prompt}")
        data = fetch_description(prompt)
        st.session_state.cache[prompt] = data

    # FAST IMAGE (Pollinations)
    enhanced_prompt = f"luxury hotel {prompt} ultra realistic 4k cinematic"
    image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced_prompt)}"
    add_debug_log(f"Generated image URL: {image_url}")
    st.session_state.generated_data = {
        "prompt": prompt,
        "data": data,
        "image_url": image_url
    }
    try:
        st.session_state.generated_image_bytes = fetch_image_bytes_with_retry(image_url)
        add_debug_log(
            f"Image bytes loaded successfully: {len(st.session_state.generated_image_bytes)} bytes"
        )
    except Exception as e:
        add_debug_log(f"Image fetch failed: {str(e)}")
        st.session_state.generated_image_bytes = None
    st.session_state.show_generated_image = True

    # SAVE HISTORY
    if prompt not in st.session_state.history:
        st.session_state.history.append(prompt)

# ------------------ RENDER RESULT ------------------
if st.session_state.generated_data:
    data = st.session_state.generated_data["data"]
    image_url = st.session_state.generated_data["image_url"]
    col1, col2 = st.columns(2)

    # ---------------- IMAGE ----------------
    with col1:
        st.markdown("### 🖼️ AI Design")

        if st.session_state.show_generated_image and st.session_state.generated_image_bytes:
            st.image(st.session_state.generated_image_bytes, width="stretch")
        elif st.session_state.show_generated_image:
            st.warning("Image could not be previewed. Check debug logs below.")

        try:
            img_bytes = st.session_state.generated_image_bytes
            if not img_bytes:
                raise ValueError("Image bytes unavailable")
            download_clicked = st.download_button(
                "📥 Download",
                img_bytes,
                file_name="design.png",
                mime="image/png"
            )
            if download_clicked:
                add_debug_log("Download button clicked; hiding current preview image")
                st.session_state.show_generated_image = False
        except Exception as e:
            add_debug_log(f"Download preparation failed: {str(e)}")
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

# ------------------ HISTORY ------------------
st.markdown("### 🕒 History")
for item in st.session_state.history[::-1]:
    st.markdown(f"- {item}")

# ------------------ DEBUG LOGS ------------------
with st.expander("🪵 Debug Logs", expanded=False):
    if st.button("Clear Logs"):
        st.session_state.debug_logs = []
    if st.session_state.debug_logs:
        st.code("\n".join(st.session_state.debug_logs[-100:]))
    else:
        st.caption("No logs yet.")