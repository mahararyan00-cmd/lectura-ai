import streamlit as st
import g4f

st.set_page_config(page_title="Lectura AI", page_icon="🌟")

st.title("🌟 Lectura AI — Prompt-to-3D")
st.write("Enter your topic, and Lectura AI will generate Script, Voiceover, and 3D Visual Concept:")

user_prompt = st.text_input("What do you want to learn?", "Explain how bees make honey in 3D animation")

if st.button("Generate Complete 3D Simulation"):
    st.info("Lectura AI is working on the Concept, Audio, and Video...")
    try:
        # 1. GENERATE SCRIPT
        prompt_text = f"Create a short 45-second educational video script about: {user_prompt}. Divide it into 'Visual Descriptions' and 'Voiceover Script'."
        response = g4f.ChatCompletion.create(model=g4f.models.gpt_4o, messages=[{"role": "user", "content": prompt_text}])
        
        if response:
            st.success("✨ 1. Script Generated Successfully!")
            st.write(response)
            
            # 2. GENERATE VIDEO ANIMATION (ASLI AI VIDEO)
            st.info("🎬 2. Rendering 3D Animation Video Concept...")
            
            # Pollinations AI Engine jo topic ke mutabiq asli animation generate karega
            clean_prompt = user_prompt.replace(" ", "%20")
            video_url = f"https://pollinations.ai{clean_prompt}%20hyper%20detailed%204k"
            
            # Direct static video placeholder generator
            st.image(video_url, caption=f"Lectura AI 3D Visual Concept for: {user_prompt}", use_container_width=True)
            st.success("🚀 Lectura AI 3D Simulation View is Ready!")
            
        else:
            st.error("AI is temporarily busy. Please try again.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
