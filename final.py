import streamlit as st
import requests
import tempfile
import time
import base64
import asyncio
import re
import edge_tts

# 1. PROFESSIONAL LOOK & THEME CONFIGURATION
st.set_page_config(page_title="Lectura AI Pro", page_icon="🌟", layout="wide")

# --- MONETIZATION & SESSION STATES ---
if "history" not in st.session_state:
    st.session_state.history = []
if "lecture_count" not in st.session_state:
    st.session_state.lecture_count = 0
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False
if "prompt_key" not in st.session_state:
    st.session_state.prompt_key = 0

PREMIUM_CODE = "LECTURA2024" 
FREE_LIMIT = 50 

# ==========================================
# 🛑 APNI DETAILS YAHAN DALEIN
# ==========================================
YOUR_EASYPAISA_NUMBER = "0300-1234567" # Apna Easypaisa/JazzCash number likhein
YOUR_WHATSAPP_LINK = "https://wa.link/n6dqm6" # Aapka WhatsApp short link
# ==========================================

# --- THEME SETTINGS ---
themes = {
    "Royal Blue": {"primary": "#4169E1", "secondary": "#1E90FF", "bg": "#050A30"},
    "Neon Blue": {"primary": "#00f2fe", "secondary": "#4facfe", "bg": "#0b0f19"},
    "Cyberpunk Purple": {"primary": "#bc13fe", "secondary": "#ff00e6", "bg": "#120b19"},
    "Matrix Green": {"primary": "#00ff41", "secondary": "#008f11", "bg": "#0b0f0b"},
    "Sunset Orange": {"primary": "#f7971e", "secondary": "#ffd200", "bg": "#19130b"}
}

def safe_rerun():
    try: st.rerun()
    except:
        try: st.experimental_rerun()
        except: pass

def clean_text_for_voice(text):
    text = re.sub(r'[\[\(].*?[\]\)]', '', text)
    text = re.sub(r'\*.*?\*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# FLOATING WHATSAPP BUTTON (Screen ke neeche right side)
st.markdown(f"""
    <a href="{YOUR_WHATSAPP_LINK}" target="_blank" style="position: fixed; bottom: 20px; right: 20px; background-color: #25D366; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); z-index: 999; text-decoration: none; font-size: 30px;">💬</a>
""", unsafe_allow_html=True)

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
    if st.button("🆕 Start New Lecture", use_container_width=True):
        st.session_state.prompt_key += 1
        safe_rerun()
    st.markdown("---")
    
    if st.session_state.history:
        for idx, hist in enumerate(st.session_state.history):
            col1, col2 = st.columns([5, 1])
            with col1: st.info(f"📝 {hist[:30]}...")
            with col2:
                if st.button("❌", key=f"del_{idx}"):
                    del st.session_state.history[idx]
                    safe_rerun()
    else: st.write("No previous lectures yet.")

    # SIDEBAR PREMIUM BANNER (PAKISTAN ONLY)
    st.markdown("---")
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, {t['primary']} 0%, {t['secondary']} 100%); padding: 20px; text-align: center; border-radius: 10px; color: black;">
            <h3 style="margin:0; color: #050A30;">👑 Get Premium!</h3>
            <p style="margin:5px 0; font-size: 14px; font-weight:bold;">Unlimited Lectures - Rs. 500</p>
            <p style="margin:0; font-size: 12px;">🇵🇰 Easypaisa/JazzCash: <b>{YOUR_EASYPAISA_NUMBER}</b></p>
            <a href="{YOUR_WHATSAPP_LINK}" target="_blank" style="background-color: #25D366; color: white; padding: 8px 15px; border-radius: 5px; text-decoration: none; display: inline-block; margin-top: 10px; font-weight: bold;">💬 WhatsApp for Code</a>
        </div>
    """, unsafe_allow_html=True)

# --- PAYWALL CHECK (PAKISTAN ONLY) ---
if not st.session_state.is_premium and st.session_state.lecture_count >= FREE_LIMIT:
    st.markdown("---")
    st.error("🚫 **Free Trial Expired!**")
    st.markdown(f"""
        <div style="background-color: #161b26; padding: 30px; border-radius: 12px; border: 2px solid #f7971e; text-align: center;">
            <h3 style="color: #f7971e;">👑 Upgrade to Premium</h3>
            <p style="color: white; font-size: 18px;">Aap ne {FREE_LIMIT} free lectures use kar li hain.</p>
            <p style="color: white; font-size: 16px;">🇵🇰 <b>Pakistan Payment:</b> Rs. 500/- Easypaisa/JazzCash par bhejein:</p>
            <h2 style="color: #00f2fe;">{YOUR_EASYPAISA_NUMBER}</h2>
            <a href="{YOUR_WHATSAPP_LINK}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; display: inline-block; margin-top: 15px; font-weight: bold; font-size: 18px;">💬 WhatsApp karein aur Code lein</a>
            <p style="color: #aaa; font-size: 14px; margin-top: 15px;">Paise bhejne ke baad WhatsApp par message karein, hum Premium Code de denge.</p>
        </div>
    """, unsafe_allow_html=True)
    
    code_input = st.text_input("🔑 Enter Premium Code:")
    if st.button("🔓 Unlock Premium"):
        if code_input == PREMIUM_CODE:
            st.session_state.is_premium = True
            st.success("🎉 Premium Activated! Unlimited lectures enjoy karein.")
            safe_rerun()
        else: st.error("❌ Invalid Code. Paise bhejein aur sahi code lein.")
    st.stop()

# Main Layout
st.title("🌟 Lectura AI Pro — Studio Dashboard")
st.write("Powered by ChatGPT Brain & Ultra-Realistic Voice")

st.markdown(f"""
    <div style="background-color: #161b26; padding: 15px; text-align: center; border-radius: 8px; border: 2px solid {t['primary']}; margin-bottom: 20px;">
        <p style="color: white; font-size: 16px; font-weight: bold; margin:0;">📚 Ace Your Exams with AI Visual Lectures & Quiz!</p>
    </div>
""", unsafe_allow_html=True)

app_mode = st.radio("🎯 Select Mode:", ("📖 Q&A Mode (Fast Answers)", "🎬 Lecture Mode (Visual Simulation)"))
language_option = st.selectbox("🎙️ Select Voiceover Language:", ("Roman Urdu", "Urdu (اردو)", "Hindi (हिन्दी)", "English", "Arabic"))

voice_codes = {"Roman Urdu": "ur-PK-AsadNeural", "Urdu (اردو)": "ur-PK-AsadNeural", "Hindi (हिन्दी)": "hi-IN-MadhurNeural", "English": "en-US-GuyNeural", "Arabic": "ar-SA-HamedNeural"}
selected_voice_code = voice_codes[language_option]

user_prompt = st.text_input("✍️ Type your question or topic here:", "Photosynthesis kya hai?", key=f"prompt_key_{st.session_state.prompt_key}")

def generate_voice(text, voice_code, filename):
    async def _save():
        communicate = edge_tts.Communicate(text, voice_code)
        await communicate.save(filename)
    asyncio.run(_save())

def ask_chatgpt_brain(prompt_text, lang="English"):
    url = "https://text.pollinations.ai/"
    payload = {"messages": [{"role": "system", "content": "You are an expert AI tutor. Follow format strictly. Write pure spoken text."}, {"role": "user", "content": prompt_text}], "model": "openai", "seed": 42}
    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=90)
            if response.status_code == 200: return response.text
            elif response.status_code == 429: time.sleep(5 * (attempt + 1))
            else: raise Exception(f"API Error {response.status_code}")
        except: time.sleep(3)
    raise Exception("Server overloaded.")

if st.button("🚀 Generate Answer / Lecture"):
    st.session_state.lecture_count += 1
    if user_prompt not in st.session_state.history: st.session_state.history.append(user_prompt)
    progress_bar = st.progress(0)
    
    st.info("⚡ ChatGPT Brain is thinking...")
    progress_bar.progress(20)
    
    try:
        base_prompt = (
            f"Topic: {user_prompt}. Language: STRICTLY {language_option}. "
            f"FORMAT (FOLLOW EXACTLY):\n"
            f"1. First line: 'IMAGE_PROMPT: ' + 1 English sentence.\n"
            f"2. Next line: '[HEADINGS_START]'\n 3-5 exam points.\n"
            f"3. Next line: '[VOICEOVER_START]'\n Detailed spoken explanation. No [music].\n"
            f"4. Next line: '[QUESTIONS_START]'\n 5 important questions related to the topic to test the student.\n"
            f"5. Next line: '[QUESTIONS_END]'"
        )
            
        result = ask_chatgpt_brain(base_prompt, lang=language_option)
        
        if result and len(result.strip()) > 10:
            image_keyword, exam_headings, voiceover_script, related_questions = user_prompt, "", result, ""
            result_clean = re.sub(r'\*+', '', result) 
            
            if "IMAGE_PROMPT:" in result_clean:
                for line in result_clean.split('\n'):
                    if line.strip().startswith("IMAGE_PROMPT:"): image_keyword = line.replace("IMAGE_PROMPT:", "").strip(); result_clean = result_clean.replace(line, "").strip()
            
            if "[HEADINGS_START]" in result_clean and "[VOICEOVER_START]" in result_clean:
                parts = result_clean.split("[HEADINGS_START]")
                if len(parts) > 1:
                    sub_parts = parts[1].split("[VOICEOVER_START]")
                    if len(sub_parts) > 1:
                        exam_headings = sub_parts[0].strip()
                        remaining_text = sub_parts[1]
                        if "[QUESTIONS_START]" in remaining_text and "[QUESTIONS_END]" in remaining_text:
                            q_parts = remaining_text.split("[QUESTIONS_START]")
                            voiceover_script = q_parts[0].strip()
                            q_sub_parts = q_parts[1].split("[QUESTIONS_END]")
                            related_questions = q_sub_parts[0].strip()
                        else: voiceover_script = remaining_text.strip()
            
            if not exam_headings: exam_headings = "Headings not generated."
            if not voiceover_script: voiceover_script = result
            if not related_questions: related_questions = "Questions not generated."

            progress_bar.progress(50)
            st.success("✨ ChatGPT Brain Answered!")
            
            voiceover_clean = clean_text_for_voice(voiceover_script)
            
            try:
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                generate_voice(voiceover_clean, selected_voice_code, temp_audio.name)
                progress_bar.progress(70); st.success("✨ Voice Synthesized!"); temp_audio_path = temp_audio.name
            except: temp_audio_path = None

            st.markdown("---")
            st.markdown(f"""<div style="background-color: #161b26; padding: 25px; border-radius: 12px; border: 2px solid {t['primary']}; margin-bottom: 20px;"><h3 style="color: {t['primary']}; margin-top:0; border-bottom: 1px solid #333; padding-bottom:10px;">🎓 Exam Preparation Headings</h3><p style="font-size: 17px; color: #ffffff; line-height: 1.6;">{exam_headings.replace(chr(10), '<br>')}</p></div>""", unsafe_allow_html=True)
            
            if app_mode == "🎬 Lecture Mode (Visual Simulation)":
                st.info("🎨 Generating 10 Visual Frames..."); time.sleep(2)
                img_urls = [f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_keyword + f' scene {i+1} 3D realistic educational cinematic')}?width=1024&height=576&nologo=true&seed={i+1}" for i in range(10)]
                progress_bar.progress(100)
                st.subheader("🛸 AI Video Simulation")
                html_template = """<div id="videoContainer" style="text-align: center; background: #000; padding: 10px; border-radius: 10px; border: 2px solid PRIMARY_COLOR;"><img id="videoSlide" src="IMG1_URL" style="width: 100%; height: auto; border-radius: 8px; opacity: 1; transition: opacity 1s ease-in-out;"><div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;"><p style="color: PRIMARY_COLOR; font-family: monospace; margin: 0;">▶ Scene: <span id="frameNum">1</span>/10</p><button onclick="toggleFullscreen()" style="background: linear-gradient(135deg, PRIMARY_COLOR 0%, SECONDARY_COLOR 100%); color: black; font-weight: bold; border: none; border-radius: 5px; padding: 8px 15px; cursor: pointer;">⛶ Fullscreen</button></div></div><script>var images = ["IMG1_URL", "IMG2_URL", "IMG3_URL", "IMG4_URL", "IMG5_URL", "IMG6_URL", "IMG7_URL", "IMG8_URL", "IMG9_URL", "IMG10_URL"];var current = 0;var imgElement = document.getElementById("videoSlide");var frameNum = document.getElementById("frameNum");setInterval(function() {imgElement.style.opacity = 0;setTimeout(function() {current = (current + 1) % images.length;imgElement.src = images[current];frameNum.innerText = current + 1;imgElement.style.opacity = 1;}, 1000);}, 5000);function toggleFullscreen() {var elem = document.getElementById('videoContainer');if (!document.fullscreenElement) {if (elem.requestFullscreen) { elem.requestFullscreen(); }} else {if (document.exitFullscreen) { document.exitFullscreen(); }}}</script>"""
                final_html = html_template.replace("PRIMARY_COLOR", t['primary']).replace("SECONDARY_COLOR", t['secondary'])
                for i, url in enumerate(img_urls): final_html = final_html.replace(f"IMG{i+1}_URL", url)
                st.components.v1.html(final_html, height=500)
                st.markdown("---")
            else: progress_bar.progress(100); st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"🎬 AI Voiceover Script ({language_option})")
                st.write(voiceover_script)
                st.markdown("### 📥 Save & Share Options")
                dl_col1, dl_col2, dl_col3 = st.columns(3)
                with dl_col1: st.download_button(label="📄 Download Script", data=voiceover_script, file_name="Lectura_AI_Script.txt", mime="text/plain")
                with dl_col2:
                    if temp_audio_path:
                        with open(temp_audio_path, "rb") as f: audio_bytes = f.read()
                        st.download_button(label="🎧 Download Audio", data=audio_bytes, file_name="Lectura_AI_Voice.mp3", mime="audio/mp3")
                with dl_col3:
                    if st.button("📋 Copy Text"): st.markdown(f"""<script>navigator.clipboard.writeText(`{voiceover_script.replace('`', "'")}`);</script>""", unsafe_allow_html=True); st.success("Copied!")
            
            with col2:
                st.subheader("🎙️ Ultra-Realistic AI Voice (Male)")
                if temp_audio_path: st.audio(temp_audio_path, format="audio/mp3")
                
                st.markdown("---")
                st.subheader("❓ Test Yourself (Related Questions)")
                st.markdown(f"""
                    <div style="background-color: #1a1f2e; padding: 20px; border-radius: 10px; border-left: 5px solid #f7971e; color: white; font-size: 16px; line-height: 1.8;">
                        {related_questions.replace(chr(10), '<br>')}
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.subheader("💬 Still Confused? Ask Below")
                follow_up = st.text_input("Ask a follow-up question:", key="follow_up_input")
                if follow_up:
                    chat_result = ask_chatgpt_brain(f"About '{user_prompt}', answer briefly in {language_option}: {follow_up}")
                    chat_clean = clean_text_for_voice(chat_result)
                    temp_chat_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    generate_voice(chat_clean, selected_voice_code, temp_chat_audio.name)
                    st.markdown(f"<div class='chat-box'><b>You:</b> {follow_up}<br><br><b>ChatGPT AI:</b> {chat_result}</div>", unsafe_allow_html=True)
                    st.audio(temp_chat_audio.name, format="audio/mp3")
        else: st.error("⚠️ AI returned empty.")
    except Exception as e: st.error(f"Execution Error: {e}")
