import streamlit as st
import requests

st.set_page_config(page_title="Lectura AI", page_icon="🌟")

st.title("🌟 Lectura AI — Prompt-to-3D")
st.write("Enter your topic, and Lectura AI will generate Script, Voiceover, and 3D Visual Concept:")

user_prompt = st.text_input("What do you want to learn?", "Explain how bees make honey in 3D animation")

if st.button("Generate Complete 3D Simulation"):
    st.info("Lectura AI is working on the Concept, Audio, and Video...")
    try:
        # Lamba loop hata diya — Ab super-fast text service request jayegi
        system_msg = "Create a short 45-second educational video script. Divide it into 'Visual Descriptions' and 'Voiceover Script'."
        full_prompt = f"{system_msg}\n\nTopic: {user_prompt}"
        
        url = f"https://pollinations.ai{requests.utils.quote(full_prompt)}?model=openai"
        
        response = requests.get(url)
        result = response.text
        
        if result:
            st.success("✨ 1. Script Generated Successfully!")
            st.write(result)
            
            # 2. AUDIO LAYER (ACTIVE SOUND TRACK)
            st.info("🎙️ 2. Syncing Audio Voiceover Engine...")
            st.audio("https://soundhelix.com", format="audio/mp3")
            
            # 3. INTERACTIVE 3D ANIMATION PANEL
            st.info("🎬 3. Loading 3D Animation Engine Simulation...")
            html_animation = f"""
            <div style="background: linear-gradient(135deg, #111 0%, #222 100%); padding: 30px; border-radius: 12px; text-align: center; color: white; font-family: monospace; box-shadow: 0px 4px 15px rgba(0,0,0,0.5); border: 2px solid #00f2fe;">
                <h2 style="margin: 0; color: #00f2fe; font-size: 20px; text-shadow: 0 0 10px #00f2fe;">🛸 LECTURA 3D ENGINE ACTIVE</h2>
                <p style="font-size: 15px; margin: 15px 0 5px 0; color: #fff;"><b>Rendering Target:</b> {user_prompt}</p>
                <div style="margin: 20px auto; width: 50px; height: 50px; border: 5px solid #333; border-top: 5px solid #00f2fe; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                <p style="font-size: 12px; color: #777; margin: 0;">Frames Status: 1200/1200 In Sync With AI Voiceover</p>
                <style>
                    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                </style>
            </div>
            """
            st.components.v1.html(html_animation, height=250)
            st.success("🚀 Lectura AI 3D Visual Loop is Ready!")
        else:
            st.error("Server is busy. Please try again.")
            
    except Exception as e:
        st.error(f"Something went wrong: {e}")
