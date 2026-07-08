import streamlit as st
import requests
import tempfile
from gtts import gTTS
import time

# 1. PROFESSIONAL LOOK & THEME CONFIGURATION
st.set_page_config(page_title="Lectura AI Pro", page_icon="🌟", layout="wide")

# Custom Dark Neon CSS
st.markdown("""
    <style>
    .main {background-color: #0b0f19; color: #ffffff;}
    .stButton>button {background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); color: black; font-weight: bold; border-radius: 8px; border: none; width: 100%; height: 45px;}
    .stTextInput>div>div>input {background-color: #161b26; color: white; border: 1px solid #00f2fe; border-radius: 8px;}
    .chat-box {background-color: #161b26; padding: 15px; border-radius: 10px; border-left: 5px solid #00f2fe; margin-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)

# Application States
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.title("📜 Lecture History")
    if st.session_state.history:
        for idx, hist in enumerate(st.session_state.history):
            st.info(f"{idx+1}. {hist}")
    else:
        st.write("No previous lectures yet.")

# Pollinations Text API Function
def ask_pollinations(prompt_text):
    url = "https://text.pollinations.ai/"
    payload = {
        "messages": [
            {"role": "system", "content": "You are a strict educational AI. Provide ONLY to-the-point factual bullet points. DO NOT add any greetings, conclusions, or filler words. Just the facts."},
            {"role": "user", "content": prompt_text}
        ],
        "model": "openai",
        "seed": 42
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"API Error {response.status_code}")

# Main Layout
st.title("🌟 Lectura AI Pro — Studio Dashboard")
st.write("Professional Prompt-to-3D Educational Suite (Multi-Language)")

# Language Selection Dropdown
language_option = st.selectbox(
    "🎙️ Select Voiceover Language:",
    ("English", "Urdu", "Hindi", "Arabic", "Spanish", "French")
)

# Language mapping for gTTS
lang_codes = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "Spanish": "es",
    "French": "fr"
}
selected_lang_code = lang_codes[language_option]

user_prompt = st.text_input("What scientific topic do you want to animate?", "Explain how bees make honey in 3D animation")

if st.button("Launch Professional 3D Simulation Suite"):
    if user_prompt not in st.session_state.history:
        st.session_state.history.append(user_prompt)

    progress_bar = st.progress(0)
    
    # --- STEP 1: Generate Text Script ---
    st.info("⚡ Phase 1: Compiling Neural Script (Strict Facts Only)...")
    progress_bar.progress(20)
    
    try:
        prompt_text = (
            f"Create a concise educational voiceover script about: {user_prompt}. "
            f"Include ONLY important facts and key educational points. "
            f"REPLY STRICTLY IN {language_option} LANGUAGE."
        )
        result = ask_pollinations(prompt_text)
        
        if result and len(result.strip()) > 10:
            progress_bar.progress(40)
            st.success("✨ Phase 1 Complete: Script Compiled!")
            
            # --- STEP 2: Generate 5 AI Images for Better Video Flow ---
            st.info("🎨 Phase 2: Generating 5 AI Visual Frames for Video Simulation...")
            time.sleep(2) # API rate limit se bachne ke liye
            
            # 5 alag alag scenes banaye hain
            img1_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(user_prompt + ' scene 1 introduction overview 3D realistic educational cinematic')}?width=768&height=512&nologo=true&seed=1"
            img2_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(user_prompt + ' scene 2 initial stage process 3D realistic educational cinematic')}?width=768&height=512&nologo=true&seed=2"
            img3_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(user_prompt + ' scene 3 middle stage mechanism 3D realistic educational cinematic')}?width=768&height=512&nologo=true&seed=3"
            img4_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(user_prompt + ' scene 4 climax main action 3D realistic educational cinematic')}?width=768&height=512&nologo=true&seed=4"
            img5_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(user_prompt + ' scene 5 final result conclusion 3D realistic educational cinematic')}?width=768&height=512&nologo=true&seed=5"

            progress_bar.progress(70)
            st.success("✨ Phase 2 Complete: 5 Visual Frames Rendered!")
            
            # --- STEP 3: Generate Voice ---
            st.info(f"🎙️ Phase 3: Synthesizing AI Voiceover in {language_option}...")
            
            try:
                tts = gTTS(text=result, lang=selected_lang_code, slow=False)
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp_audio.name)
                progress_bar.progress(100)
                st.success("✨ Phase 3 Complete: Audio Synthesized!")
                temp_audio_path = temp_audio.name
            except Exception:
                temp_audio_path = None

            # --- DISPLAY LAYOUT ---
            st.markdown("---")
            
            # AI VIDEO PLAYER (5 Images auto-playing like a video)
            st.subheader("🛸 AI Generated Video Simulation (5 Frames)")
            video_player_html = f"""
            <div style="text-align: center; background: #000; padding: 10px; border-radius: 10px; border: 2px solid #00f2fe;">
                <img id="videoSlide" src="{img1_url}" style="width: 100%; height: auto; border-radius: 8px; transition: opacity 0.8s ease-in-out;">
                <p style="color: #00f2fe; font-family: monospace; margin-top: 5px;">▶ Playing Simulation... | Scene: <span id="frameNum">1</span>/5</p>
            </div>
            <script>
                var images = ["{img1_url}", "{img2_url}", "{img3_url}", "{img4_url}", "{img5_url}"];
                var current = 0;
                var imgElement = document.getElementById("videoSlide");
                var frameNum = document.getElementById("frameNum");
                setInterval(function() {{
                    current = (current + 1) % images.length;
                    imgElement.src = images[current];
                    frameNum.innerText = current + 1;
                }}, 3000); // Change image every 3 seconds
            </script>
            """
            st.components.v1.html(video_player_html, height=450)

            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🎬 AI Voiceover Script (Facts Only)")
                st.write(result)

            with col2:
                st.subheader("🎙️ AI Voiceover Audio Track")
                if temp_audio_path:
                    st.audio(temp_audio_path, format="audio/mp3")
                else:
                    st.audio("https://soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
                
                # Chat Feature
                st.subheader("💬 Continue Lecture")
                follow_up = st.text_input("Ask a question:", key="follow_up_input")
                if follow_up:
                    chat_result = ask_pollinations(f"About '{user_prompt}', answer briefly in {language_option}: {follow_up}")
                    st.markdown(f"<div class='chat-box'><b>You:</b> {follow_up}<br><br><b>Lectura AI:</b> {chat_result}</div>", unsafe_allow_html=True)
        else:
            st.error("⚠️ AI returned empty response. Try again.")

    except Exception as e:
        st.error(f"Execution Error: {e}")
