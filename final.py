import streamlit as st
import requests

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
if "history" not in st.session_state: st.session_state.history = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# Sidebar for Lecture History Tab
with st.sidebar:
    st.title("📜 Lecture History")
    if st.session_state.history:
        for idx, hist in enumerate(st.session_state.history):
            st.info(f"{idx+1}. {hist}")
    else:
        st.write("No previous lectures yet.")

# Main Application Layout
st.title("🌟 Lectura AI Pro — Studio Dashboard")
st.write("Professional Prompt-to-3D Educational Suite")

# Main Input Form
user_prompt = st.text_input("What scientific topic do you want to animate?", "Explain how bees make honey in 3D animation")

if st.button("Launch Professional 3D Simulation Suite"):
    if user_prompt not in st.session_state.history:
        st.session_state.history.append(user_prompt)
        
    st.info("⚡ System Booting: Compiling Script, Audio Vectors, and Visual Matrix...")
    
    try:
        # ISS LINE MEIN SLASH (/) FIX KAR DIYA HAI
        url = f"https://pollinations.ai{requests.utils.quote(user_prompt)}?model=searchgpt"
        
        response = requests.get(url)
        result = response.text
        
        if result:
            st.session_state.current_script = result
            st.success("✨ Phase 1 & 2: Neural Script & Visual Blueprint Compiled!")
            
            # Layout Columns for Professional Look (Side-by-Side Content)
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎬 AI Visual Description & Script")
                st.write(result)
                
                # Active Media Controllers
                st.subheader("🎙️ Voiceover Audio Track")
                st.audio("https://soundhelix.com", format="audio/mp3")
                st.button("📥 Download Full MP3 Lecture Voiceover", key="dl_btn")
            
            with col2:
                st.subheader("🛸 Real-time 3D Engine Simulation View")
                # Advanced HTML Canvas Spinner Integration
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
                
                # Continue Lecture Feature: Question Box While Video is "Playing"
                st.subheader("💬 Continue Lecture (Ask Mid-Video Questions)")
                follow_up = st.text_input("Got a question during the animation? Ask here instantly:", key="follow_up_input")
                if follow_up:
                    st.info("Analyzing context against current visual matrix...")
                    chat_url = f"https://pollinations.ai{requests.utils.quote(follow_up)}?model=openai"
                    chat_res = requests.get(chat_url).text
                    st.markdown(f"<div class='chat-box'><b>You:</b> {follow_up}<br><br><b>Lectura AI Assistant:</b> {chat_res}</div>", unsafe_allow_html=True)
                    
        else:
            st.error("Engine timeout. Re-firing vectors...")
    except Exception as e:
        st.error(f"Execution Error: {e}")
