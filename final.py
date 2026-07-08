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
            {"role": "system", "content": "You are a strict educational AI. Provide ONLY to-the-point factual bullet points. DO NOT add any greetings, conclusions, or filler words."},
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
    ("Roman Urdu", "Urdu (اردو)", "Hindi (हिन्दी)", "English", "Arabic")
)

# Language mapping for gTTS
lang_codes = {
    "Roman Urdu": "ur",
    "Urdu (اردو)": "ur",
    "Hindi (हिन्दी)": "hi",
    "English": "en",
    "Arabic": "ar"
}
selected_lang_code = lang_codes[language_option]

user_prompt = st.text_input("What scientific topic do you want to animate?", "honey kaise banta hai")

if st.button("Launch Professional 3D Simulation Suite"):
    if user_prompt not in st.session_state.history:
        st.session_state.history.append(user_prompt)

    progress_bar = st.progress(0)
    
    # --- STEP 1: Generate Script & English Image Keyword ---
    st.info("⚡ Phase 1: Compiling Neural Script & Visual Keywords...")
    progress_bar.progress(10)
    
    try:
        prompt_text = (
            f"Create a concise educational voiceover script about: {user_prompt}. "
            f"Include ONLY important facts and key educational points. "
            f"YOU MUST REPLY STRICTLY IN {language_option} LANGUAGE. "
            f"VERY IMPORTANT: On the very first line of your response, write a short 1-sentence English description of this topic for an image generator. Start that line exactly with 'IMAGE_PROMPT: '. The rest of the response must be the voiceover script."
        )
        result = ask_pollinations(prompt_text)
        
        if result and len(result.strip()) > 10:
            image_keyword = user_prompt 
            voiceover_script = result
            
            if "IMAGE_PROMPT:" in result:
                lines = result.split('\n')
                for line in lines:
                    if line.strip().startswith("IMAGE_PROMPT:"):
                        image_keyword = line.replace("IMAGE_PROMPT:", "").strip()
                        voiceover_script = result.replace(line, "").strip()
                        break

            progress_bar.progress(30)
            st.success("✨ Phase 1 Complete: Script Compiled!")
            
            # --- STEP 2: Generate 10 AI Images ---
            st.info("🎨 Phase 2: Generating 10 AI Visual Frames (This may take a moment)...")
            time.sleep(2) 
            
            # 10 Scenes banaye hain
            img1_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 1 introduction overview 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=1"
            img2_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 2 initial stage 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=2"
            img3_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 3 early process 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=3"
            img4_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 4 middle mechanism 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=4"
            img5_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 5 core action 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=5"
            img6_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 6 ongoing process 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=6"
            img7_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 7 detailed closeup 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=7"
            img8_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 8 near completion 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=8"
            img9_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 9 final result 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=9"
            img10_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + ' scene 10 ultimate conclusion 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed=10"

            progress_bar.progress(70)
            st.success("✨ Phase 2 Complete: 10 Visual Frames Rendered!")
            
            # --- STEP 3: Generate Voice ---
            st.info(f"🎙️ Phase 3: Synthesizing AI Voiceover in {language_option}...")
            
            try:
                tts = gTTS(text=voiceover_script, lang=selected_lang_code, slow=False)
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp_audio.name)
                progress_bar.progress(100)
                st.success("✨ Phase 3 Complete: Audio Synthesized!")
                temp_audio_path = temp_audio.name
            except Exception:
                temp_audio_path = None

            # --- DISPLAY LAYOUT ---
            st.markdown("---")
            
            # AI VIDEO PLAYER WITH FULLSCREEN BUTTON
            st.subheader("🛸 AI Generated Video Simulation (10 Frames)")
            video_player_html = f"""
            <div id="videoContainer" style="text-align: center; background: #000; padding: 10px; border-radius: 10px; border: 2px solid #00f2fe; position: relative;">
                <img id="videoSlide" src="{img1_url}" style="width: 100%; height: auto; border-radius: 8px; transition: opacity 0.8s ease-in-out;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                    <p style="color: #00f2fe; font-family: monospace; margin: 0;">▶ Playing Simulation... | Scene: <span id="frameNum">1</span>/10</p>
                    <button onclick="toggleFullscreen()" style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); color: black; font-weight: bold; border: none; border-radius: 5px; padding: 8px 15px; cursor: pointer;">⛶ Fullscreen</button>
                </div>
            </div>
            <script>
                var images = ["{img1_url}", "{img2_url}", "{img3_url}", "{img4_url}", "{img5_url}", "{img6_url}", "{img7_url}", "{img8_url}", "{img9_url}", "{img10_url}"];
                var current = 0;
                var imgElement = document.getElementById("videoSlide");
                var frameNum = document.getElementById("frameNum");
                setInterval(function() {{
                    current = (current + 1) % images.length;
                    imgElement.src = images[current];
                    frameNum.innerText = current + 1;
                }}, 4000); // Change image every 4 seconds for better viewing
                
                function toggleFullscreen() {{
                    var elem = document.getElementById('videoContainer');
                    if (!document.fullscreenElement) {{
                        if (elem.requestFullscreen) {{
                            elem.requestFullscreen();
                        }} else if (elem.webkitRequestFullscreen) {{ /* Safari */
                            elem.webkitRequestFullscreen();
                        }}
                    }} else {{
                        if (document.exitFullscreen) {{
                            document.exitFullscreen();
                        }}
                    }}
                }}
            </script>
            """
            st.components.v1.html(video_player_html, height=500)

            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"🎬 AI Voiceover Script ({language_option})")
                st.write(voiceover_script)

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
