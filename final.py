import streamlit as st
import requests
import tempfile
from gtts import gTTS
from langdetect import detect

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
            {"role": "system", "content": "You are an expert educational AI. Provide ONLY important facts, key points, and essential lecture notes. Remove all fluff, greetings, and filler words."},
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

user_prompt = st.text_input("What scientific topic do you want to animate?", "Explain how bees make honey in 3D animation")

if st.button("Launch Professional 3D Simulation Suite"):
    if user_prompt not in st.session_state.history:
        st.session_state.history.append(user_prompt)

    progress_bar = st.progress(0)
    
    # --- STEP 1: Generate Text Script (Multi-Language) ---
    st.info("⚡ Phase 1: Compiling Neural Script & Detecting Language...")
    progress_bar.progress(20)
    
    try:
        # Detect user's language
        detected_lang = detect(user_prompt)
        
        prompt_text = (
            f"Create a concise educational lecture voiceover about: {user_prompt}. "
            f"Include ONLY important facts and key educational points. "
            f"YOU MUST REPLY IN THE SAME LANGUAGE AS THE PROMPT (Language code: {detected_lang})."
        )
        result = ask_pollinations(prompt_text)
        
        if result and len(result.strip()) > 10:
            progress_bar.progress(50)
            st.success("✨ Phase 1 Complete: Script Compiled!")
            
            # --- STEP 2: Generate AI Storyboard (3 Images for Video Feel) ---
            st.info("🎨 Phase 2: Generating AI Visual Storyboard (3 Frames)...")
            
            col_img1, col_img2, col_img3 = st.columns(3)
            
            with col_img1:
                img1_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(user_prompt + ' beginning phase 3D realistic educational')}?width=512&height=512&nologo=true"
                
            with col_img2:
                img2_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(user_prompt + ' middle process phase 3D realistic educational')}?width=512&height=512&nologo=true"
                
            with col_img3:
                img3_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(user_prompt + ' final result phase 3D realistic educational')}?width=512&height=512&nologo=true"

            progress_bar.progress(75)
            st.success("✨ Phase 2 Complete: Visual Matrix Rendered!")
            
            # --- STEP 3: Generate Multi-Language Voice ---
            st.info("🎙️ Phase 3: Synthesizing AI Voiceover in your Language...")
            
            try:
                # gTTS automatically handles languages like Hindi (hi), Urdu (ur), English (en), etc.
                tts = gTTS(text=result, lang=detected_lang, slow=False)
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp_audio.name)
                
                progress_bar.progress(100)
                st.success("✨ Phase 3 Complete: Audio Synthesized!")
                temp_audio_path = temp_audio.name
            except Exception as audio_err:
                # Fallback if language not supported by gTTS
                st.warning(f"Voice generation in detected language failed, trying English: {audio_err}")
                try:
                    tts = gTTS(text=result, lang='en', slow=False)
                    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tts.save(temp_audio.name)
                    temp_audio_path = temp_audio.name
                except:
                    temp_audio_path = None

            # --- DISPLAY LAYOUT ---
            st.markdown("---")
            st.subheader("🎬 AI Voiceover Script (Important Lecture Notes)")
            st.write(result)

            st.subheader("🎙️ AI Voiceover Audio Track")
            if temp_audio_path:
                st.audio(temp_audio_path, format="audio/mp3")
            else:
                st.audio("https://soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")

            st.markdown("---")
            st.subheader("🛸 AI Visual Storyboard (Video Concept Frames)")
            # Display the 3 images
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(img1_url, caption="Frame 1: Start", use_container_width=True)
            with col2:
                st.image(img2_url, caption="Frame 2: Process", use_container_width=True)
            with col3:
                st.image(img3_url, caption="Frame 3: Result", use_container_width=True)
                
            st.markdown("---")
            # Chat Feature
            st.subheader("💬 Continue Lecture (Ask Questions)")
            follow_up = st.text_input("Ask a question about this topic:", key="follow_up_input")
            if follow_up:
                st.info("Analyzing context...")
                chat_result = ask_pollinations(f"About the topic '{user_prompt}', answer briefly: {follow_up}")
                st.markdown(f"<div class='chat-box'><b>You:</b> {follow_up}<br><br><b>Lectura AI:</b> {chat_result}</div>", unsafe_allow_html=True)
        else:
            st.error("⚠️ AI returned empty response. Try again.")

    except Exception as e:
        st.error(f"Execution Error: {e}")
