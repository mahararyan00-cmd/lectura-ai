import streamlit as st
import requests
import json

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

# Application States for Chat and History
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# Sidebar for Lecture History Tab
with st.sidebar:
    st.title("📜 Lecture History")
    if st.session_state.history:
        for idx, hist in enumerate(st.session_state.history):
            st.info(f"{idx+1}. {hist}")
    else:
        st.write("No previous lectures yet.")

# ============================================================
# CORRECT POLLINATIONS API FUNCTION (YEH MAIN FIX HAI)
# ============================================================
def ask_pollinations(prompt_text):
    """
    Pollinations AI ko sahi tarika se call karta hai.
    POST request use karte hain taake prompt properly bhej sakein.
    """
    url = "https://text.pollinations.ai/"
    
    # Yeh POST request hai - prompt body mein jaayega, URL mein nahi
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an expert educational scriptwriter. Create detailed, engaging educational content."
            },
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        "model": "openai",
        "seed": 42
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"API Error {response.status_code}: {response.text[:200]}")


# Main Application Layout
st.title("🌟 Lectura AI Pro — Studio Dashboard")
st.write("Professional Prompt-to-3D Educational Suite")

# Main Input Form
user_prompt = st.text_input(
    "What scientific topic do you want to animate?",
    "Explain how bees make honey in 3D animation"
)

if st.button("Launch Professional 3D Simulation Suite"):
    if user_prompt not in st.session_state.history:
        st.session_state.history.append(user_prompt)

    st.info("⚡ System Booting: Compiling Script, Audio Vectors, and Visual Matrix...")

    try:
        # ============================================================
        # SAHI PROMPT - Short aur clear
        # ============================================================
        prompt_text = (
            f"Create a short 45-second educational video script about: {user_prompt}. "
            f"Divide your response into two clear sections:\n"
            f"1. VISUAL CONCEPT: Describe what the 3D animation should show\n"
            f"2. VOICEOVER DIALOGUE: Write the narration text\n"
            f"Keep it concise and educational."
        )

        # SAHI API CALL - POST request use karo
        result = ask_pollinations(prompt_text)

        if result and len(result.strip()) > 10:
            st.success("✨ Phase 1 & 2: Neural Script & Visual Blueprint Compiled!")

            # Layout Columns for Professional Look
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🎬 AI Visual Description & Script")
                st.write(result)

                # Active Media Controllers
                st.subheader("🎙️ Voiceover Audio Track")
                st.audio("https://soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
                st.button("📥 Download Full MP3 Lecture Voiceover", key="dl_btn")

            with col2:
                st.subheader("🛸 Real-time 3D Engine Simulation View")
                html_code = f"""
                <div style="background: linear-gradient(135deg, #111424 0%, #060814 100%); padding: 30px; border-radius: 12px; text-align: center; color: white; font-family: monospace; border: 2px solid #00f2fe; box-shadow: 0 0 20px rgba(0,242,254,0.2);">
                    <h3 style="margin: 0; color: #00f2fe; text-shadow: 0 0 10px #00f2fe;">3D CORE ENGINE: ACTIVE</h3>
                    <p style="font-size: 14px; margin: 15px 0; color: #bdc3c7;">Target Vector: <b>{user_prompt}</b></p>
                    <div style="margin: 25px auto; width: 60px; height: 60px; border: 4px solid #161b26; border-top: 4px solid #00f2fe; border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
                    <p style="font-size: 11px; color: #555;">FPS: 60.0 | Resolution: 4K UHD | Status: Streaming Matrix</p>
                    <style> @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }} </style>
                </div>
                """
                st.components.v1.html(html_code, height=260)

                # Continue Lecture Feature: Live Q&A Box
                st.subheader("💬 Continue Lecture (Ask Mid-Video Questions)")
                follow_up = st.text_input(
                    "Got a question during the animation? Ask here instantly:",
                    key="follow_up_input"
                )
                if follow_up:
                    st.info("Analyzing context against current visual matrix...")
                    try:
                        chat_result = ask_pollinations(
                            f"About the topic '{user_prompt}', answer this question briefly: {follow_up}"
                        )
                        st.markdown(
                            f"<div class='chat-box'><b>You:</b> {follow_up}<br><br>"
                            f"<b>Lectura AI Assistant:</b> {chat_result}</div>",
                            unsafe_allow_html=True
                        )
                    except Exception as chat_err:
                        st.error(f"Chat Error: {chat_err}")
        else:
            st.error("⚠️ AI returned empty response. Please try again.")

    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Server is busy — please try again in 30 seconds.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Connection failed. Check your internet connection.")
    except Exception as e:
        st.error(f"Execution Error: {e}")
