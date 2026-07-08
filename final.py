import streamlit as st
import requests
import tempfile
from gtts import gTTS

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
            {"role": "system", "content": "You are an expert educational scriptwriter. Create detailed, engaging educational content."},
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
st.write("Professional Prompt-to-3D Educational Suite")

user_prompt = st.text_input("What scientific topic do you want to animate?", "Explain how bees make honey in 3D animation")

if st.button("Launch Professional 3D Simulation Suite"):
    if user_prompt not in st.session_state.history:
        st.session_state.history.append(user_prompt)

    # Progress Bar for Professional Feel
    progress_bar = st.progress(0)
    
    # --- STEP 1: Generate Text Script ---
    st.info("⚡ Phase 1: Compiling Neural Script...")
    progress_bar.progress(25)
    
    try:
        prompt_text = (
            f"Create a short educational lecture script about: {user_prompt}. "
            f"Write a clear and engaging narration voiceover. Keep it under 150 words."
        )
        result = ask_pollinations(prompt_text)
        
        if result and len(result.strip()) > 10:
            progress_bar.progress(50)
            st.success("✨ Phase 1 Complete: Script Compiled!")
            
            # --- STEP 2: Generate AI Image ---
            st.info("🎨 Phase 2: Generating AI Visual Concept...")
            # Pollinations Image API
            image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(user_prompt + ' 3D realistic educational animation')}?width=800&height=600&nologo=true"
            
            progress_bar.progress(75)
            st.success("✨ Phase 2 Complete: Visual Matrix Rendered!")
            
            # --- STEP 3: Generate AI Voice ---
            st.info("🎙️ Phase 3: Synthesizing Human-like AI Voiceover...")
            try:
                # gTTS se audio file generate karna
                tts = gTTS(text=result, lang='en', slow=False)
                # Temporary file save karna
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp_audio.name)
                
                progress_bar.progress(100)
                st.success("✨ Phase 3 Complete: Audio Synthesized!")
                
            except Exception as audio_err:
                st.warning(f"Voice generation failed: {audio_err}. Playing backup music.")
                temp_audio = None

            # --- DISPLAY LAYOUT ---
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🎬 AI Voiceover Script")
                st.write(result)

                st.subheader("🎙️ AI Voiceover Audio Track")
                if temp_audio:
                    st.audio(temp_audio.name, format="audio/mp3")
                else:
                    st.audio("https://soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")

            with col2:
                st.subheader("🛸 AI Generated 3D Visual Concept")
                # Neeche wali line REAL AI image generate karegi
                st.image(image_url, caption=f"AI Visual: {user_prompt}", use_container_width=True)
                
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
