import streamlit as st
import requests
import tempfile
import time
import base64
import asyncio
import edge_tts
from PIL import Image

# 1. PROFESSIONAL LOOK & THEME CONFIGURATION
st.set_page_config(page_title="Lectura AI Pro", page_icon="🌟", layout="wide")

# --- THEME SETTINGS ---
themes = {
    "Royal Blue": {"primary": "#4169E1", "secondary": "#1E90FF", "bg": "#050A30"},
    "Neon Blue": {"primary": "#00f2fe", "secondary": "#4facfe", "bg": "#0b0f19"},
    "Cyberpunk Purple": {"primary": "#bc13fe", "secondary": "#ff00e6", "bg": "#120b19"},
    "Matrix Green": {"primary": "#00ff41", "secondary": "#008f11", "bg": "#0b0f0b"},
    "Sunset Orange": {"primary": "#f7971e", "secondary": "#ffd200", "bg": "#19130b"}
}

# Safe Rerun Function
def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# Sidebar
with st.sidebar:
    st.title("⚙️ App Settings")
    
    selected_theme = st.selectbox("🎨 Select Theme Color:", list(themes.keys()))
    t = themes[selected_theme]
    
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"], .stApp {{background-color: {t['bg']} !important; color: #ffffff !important;}}
        .stButton>button {{background: linear-gradient(135deg, {t['primary']} 0%, {t['secondary']} 100%); color: black; font-weight: bold; border-radius: 8px; border: none; width: 100%; height: 45px;}}
        .stTextInput>div>div>input {{background-color: #161b26; color: white; border: 1px solid {t['primary']}; border-radius: 8px;}}
        .chat-box {{background-color: #161b26; padding: 15px; border-radius: 10px; border-left: 5px solid {t['primary']}; margin-bottom: 10px;}}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.title("📜 Lecture History")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.history:
        for idx, hist in enumerate(st.session_state.history):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.info(f"📝 {hist[:30]}...")
            with col2:
                if st.button("❌", key=f"del_{idx}"):
                    del st.session_state.history[idx]
                    safe_rerun()
    else:
        st.write("No previous lectures yet.")

if "history" not in st.session_state:
    st.session_state.history = []

# --- ULTRA-REALISTIC EDGE-TTS VOICE FUNCTION ---
def generate_voice(text, voice_code, filename):
    async def _save():
        communicate = edge_tts.Communicate(text, voice_code)
        await communicate.save(filename)
    asyncio.run(_save())

# --- CHATGPT BRAIN API FUNCTION ---
def ask_chatgpt_brain(prompt_text, image_base64=None, lang="English"):
    url = "https://text.pollinations.ai/"
    
    if image_base64:
        user_content = [
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ]
    else:
        user_content = prompt_text
        
    payload = {
        "messages": [
            {"role": "system", "content": "You are ChatGPT, an expert AI tutor. You MUST follow the exact output format requested. Explain in very simple words. DO NOT add greetings or filler words."},
            {"role": "user", "content": user_content}
        ],
        "model": "openai",
        "seed": 42
    }
    headers = {"Content-Type": "application/json"}
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=90)
            if response.status_code == 200:
                return response.text
            elif response.status_code == 429:
                wait_time = 5 * (attempt + 1)
                st.warning(f"⏳ Server busy, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise Exception(f"API Error {response.status_code}")
        except requests.exceptions.Timeout:
            st.warning("⏱️ Timeout, retrying...")
            time.sleep(3)
            
    raise Exception("Server overloaded. Please wait 1 minute and try again.")

# Main Layout
st.title("🌟 Lectura AI Pro — Studio Dashboard")
st.write("Powered by ChatGPT Brain & Ultra-Realistic Voice")

# MODE SELECTION
app_mode = st.radio("🎯 Select Mode:", ("📖 Q&A Mode (Fast Answers)", "🎬 Lecture Mode (Visual Simulation)"))

# Language Selection
language_option = st.selectbox(
    "🎙️ Select Voiceover Language:",
    ("Roman Urdu", "Urdu (اردو)", "Hindi (हिन्दी)", "English", "Arabic")
)

voice_codes = {
    "Roman Urdu": "ur-PK-UzmaNeural",
    "Urdu (اردو)": "ur-PK-AsadNeural",
    "Hindi (हिन्दी)": "hi-IN-SwaraNeural",
    "English": "en-US-AriaNeural",
    "Arabic": "ar-SA-ZariyahNeural"
}
selected_voice_code = voice_codes[language_option]

# Input Section
col_input1, col_input2 = st.columns(2)

with col_input1:
    user_prompt = st.text_input("✍️ Type your question or topic here:", "Photosynthesis kya hai?")

with col_input2:
    uploaded_file = st.file_uploader("📷 Upload an image (Optional):", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

if st.button("🚀 Generate Answer / Lecture"):
    if user_prompt not in st.session_state.history:
        st.session_state.history.append(user_prompt if not uploaded_file else "📷 Image Question")

    progress_bar = st.progress(0)
    
    # --- PREPARE DATA ---
    image_base64_str = None
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        buf = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        img.save(buf, format="JPEG")
        with open(buf.name, "rb") as f:
            image_base64_str = base64.b64encode(f.read()).decode('utf-8')

    # --- GENERATE SCRIPT ---
    st.info("⚡ ChatGPT Brain is thinking...")
    progress_bar.progress(20)
    
    try:
        # NEW ADVANCED PROMPT FOR EXAM HEADINGS + SCRIPT SEPARATION
        base_prompt = (
            f"Topic: {user_prompt}. Language: STRICTLY {language_option}. "
            f"FORMAT RULES (FOLLOW EXACTLY):\n"
            f"1. First line must start with 'IMAGE_PROMPT: ' followed by a 1-sentence English visual description.\n"
            f"2. Next line must be '=== EXAM HEADINGS ==='. Under this, list 3-5 key exam topic headings (short bullet points).\n"
            f"3. Next line must be '=== VOICEOVER SCRIPT ==='. Under this, write the detailed educational explanation in simple words.\n"
        )
        
        if image_base64_str:
            prompt_text = f"Look at this image. {base_prompt}"
            result = ask_chatgpt_brain(prompt_text, image_base64=image_base64_str, lang=language_option)
        else:
            result = ask_chatgpt_brain(base_prompt, lang=language_option)
        
        if result and len(result.strip()) > 10:
            # --- PARSING LOGIC ---
            image_keyword = user_prompt 
            exam_headings = ""
            voiceover_script = result
            
            # Extract Image Prompt
            if "IMAGE_PROMPT:" in result:
                lines = result.split('\n')
                for line in lines:
                    if line.strip().startswith("IMAGE_PROMPT:"):
                        image_keyword = line.replace("IMAGE_PROMPT:", "").strip()
                        voiceover_script = voiceover_script.replace(line, "").strip()
                        break
            
            # Extract Exam Headings
            if "=== EXAM HEADINGS ===" in voiceover_script:
                parts = voiceover_script.split("=== EXAM HEADINGS ===")
                if "=== VOICEOVER SCRIPT ===" in parts[1]:
                    sub_parts = parts[1].split("=== VOICEOVER SCRIPT ===")
                    exam_headings = sub_parts[0].strip()
                    voiceover_script = sub_parts[1].strip()
                else:
                    exam_headings = parts[1].strip()
                    
            # Fallback if AI misses the tags
            elif "=== VOICEOVER SCRIPT ===" in voiceover_script:
                voiceover_script = voiceover_script.split("=== VOICEOVER SCRIPT ===")[1].strip()

            # If AI completely failed to separate, use whole text for voice
            if not exam_headings:
                exam_headings = "Headings not generated. Please check the script."
            if not voiceover_script:
                voiceover_script = result

            progress_bar.progress(50)
            st.success("✨ ChatGPT Brain Answered!")
            
            # --- GENERATE VOICE (ONLY FOR VOICEOVER SCRIPT) ---
            st.info(f"🎙️ Generating Realistic AI Voice in {language_option}...")
            try:
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                generate_voice(voiceover_script, selected_voice_code, temp_audio.name)
                progress_bar.progress(70)
                st.success("✨ Voice Synthesized!")
                temp_audio_path = temp_audio.name
            except Exception as e:
                st.warning(f"Voice generation failed: {e}")
                temp_audio_path = None

            # --- DISPLAY LAYOUT ---
            st.markdown("---")
            
            # --- EXAM HEADINGS SECTION (Beautiful UI Box) ---
            st.markdown(f"""
                <div style="background-color: #161b26; padding: 25px; border-radius: 12px; border: 2px solid {t['primary']}; margin-bottom: 20px; box-shadow: 0 0 15px rgba(0,0,0,0.5);">
                    <h3 style="color: {t['primary']}; margin-top:0; border-bottom: 1px solid #333; padding-bottom:10px;">🎓 Exam Preparation Headings</h3>
                    <p style="font-size: 17px; color: #ffffff; line-height: 1.6;">
                    {exam_headings.replace(chr(10), '<br>')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # IF LECTURE MODE -> GENERATE 10 IMAGES
            if app_mode == "🎬 Lecture Mode (Visual Simulation)":
                st.info("🎨 Generating 10 Visual Frames...")
                time.sleep(2) 
                
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

                progress_bar.progress(100)
                
                st.subheader("🛸 AI Video Simulation (Smooth Playback)")
                html_template = """
                <div id="videoContainer" style="text-align: center; background: #000; padding: 10px; border-radius: 10px; border: 2px solid PRIMARY_COLOR; position: relative;">
                    <img id="videoSlide" src="IMG1_URL" style="width: 100%; height: auto; border-radius: 8px; opacity: 1; transition: opacity 1s ease-in-out;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                        <p style="color: PRIMARY_COLOR; font-family: monospace; margin: 0;">▶ Playing Simulation... | Scene: <span id="frameNum">1</span>/10</p>
                        <button onclick="toggleFullscreen()" style="background: linear-gradient(135deg, PRIMARY_COLOR 0%, SECONDARY_COLOR 100%); color: black; font-weight: bold; border: none; border-radius: 5px; padding: 8px 15px; cursor: pointer;">⛶ Fullscreen</button>
                    </div>
                </div>
                <script>
                    var images = ["IMG1_URL", "IMG2_URL", "IMG3_URL", "IMG4_URL", "IMG5_URL", "IMG6_URL", "IMG7_URL", "IMG8_URL", "IMG9_URL", "IMG10_URL"];
                    var current = 0;
                    var imgElement = document.getElementById("videoSlide");
                    var frameNum = document.getElementById("frameNum");
                    setInterval(function() {
                        imgElement.style.opacity = 0;
                        setTimeout(function() {
                            current = (current + 1) % images.length;
                            imgElement.src = images[current];
                            frameNum.innerText = current + 1;
                            imgElement.style.opacity = 1;
                        }, 1000);
                    }, 5000); 
                    
                    function toggleFullscreen() {
                        var elem = document.getElementById('videoContainer');
                        if (!document.fullscreenElement) {
                            if (elem.requestFullscreen) { elem.requestFullscreen(); }
                        } else {
                            if (document.exitFullscreen) { document.exitFullscreen(); }
                        }
                    }
                </script>
                """
                final_html = html_template.replace("PRIMARY_COLOR", t['primary']).replace("SECONDARY_COLOR", t['secondary'])
                final_html = final_html.replace("IMG1_URL", img1_url).replace("IMG2_URL", img2_url).replace("IMG3_URL", img3_url).replace("IMG4_URL", img4_url).replace("IMG5_URL", img5_url).replace("IMG6_URL", img6_url).replace("IMG7_URL", img7_url).replace("IMG8_URL", img8_url).replace("IMG9_URL", img9_url).replace("IMG10_URL", img10_url)
                
                st.components.v1.html(final_html, height=500)
                st.markdown("---")

            else:
                progress_bar.progress(100)
                st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"🎬 AI Voiceover Script ({language_option})")
                st.write(voiceover_script)
                
                # --- DOWNLOAD & SHARE OPTIONS ---
                st.markdown("### 📥 Save & Share Options")
                dl_col1, dl_col2, dl_col3 = st.columns(3)
                
                with dl_col1:
                    st.download_button(
                        label="📄 Download Script",
                        data=voiceover_script,
                        file_name="Lectura_AI_Script.txt",
                        mime="text/plain"
                    )
                
                with dl_col2:
                    if temp_audio_path:
                        with open(temp_audio_path, "rb") as f:
                            audio_bytes = f.read()
                        st.download_button(
                            label="🎧 Download Audio",
                            data=audio_bytes,
                            file_name="Lectura_AI_Voice.mp3",
                            mime="audio/mp3"
                        )
                
                with dl_col3:
                    if st.button("📋 Copy Text"):
                        st.markdown(
                            f"""<script>navigator.clipboard.writeText(`{voiceover_script.replace('`', "'")}`);</script>""",
                            unsafe_allow_html=True
                        )
                        st.success("Text Copied!")

            with col2:
                st.subheader("🎙️ Ultra-Realistic AI Voice")
                if temp_audio_path:
                    st.audio(temp_audio_path, format="audio/mp3")
                
                st.subheader("💬 Ask Follow-up Question")
                follow_up = st.text_input("Ask a question:", key="follow_up_input")
                if follow_up:
                    chat_result = ask_chatgpt_brain(f"About '{user_prompt}', answer briefly in {language_option}: {follow_up}")
                    temp_chat_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    generate_voice(chat_result, selected_voice_code, temp_chat_audio.name)
                    
                    st.markdown(f"<div class='chat-box'><b>You:</b> {follow_up}<br><br><b>ChatGPT AI:</b> {chat_result}</div>", unsafe_allow_html=True)
                    st.audio(temp_chat_audio.name, format="audio/mp3")
        else:
            st.error("⚠️ AI returned empty response. Try again.")

    except Exception as e:
        st.error(f"Execution Error: {e}")
