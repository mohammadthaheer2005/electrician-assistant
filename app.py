import streamlit as st
from audio_recorder_streamlit import audio_recorder
import ai_engine
import voice_utils
import calculators
import knowledge_base
import base64

st.set_page_config(page_title="ElectroAssist Premium", page_icon="⚡", layout="wide")

# -- Premium CSS Styling --
st.markdown("""
<style>
    .reportview-container {background: #f4f6f9;}
    .sidebar .sidebar-content {background: #eef1f6;}
    h1 {color: #1E3A8A; font-family: 'Arial Black', sans-serif;}
    h2, h3 {color: #2563EB; font-family: 'Arial', sans-serif;}
    .stMetric {background-color: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .stAlert {border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Electrician Smart Assistant Premium")
st.markdown("*Your intelligent, multilingual companion for advanced electrical field work.*")

# Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=80)
st.sidebar.title("Navigation")
mode = st.sidebar.radio("Go to:", [
    "💬 Voice & Chat (గళం)",
    "🔧 Dynamic Troubleshooter",
    "📹 Live Video / Scanner",
    "⚡ Load & Gauge Finder", 
    "📏 Circuit Voltage Drop", 
    "🛠️ Winding Database"
])

# Language Configuration for Voice
st.sidebar.markdown("---")
st.sidebar.subheader("🗣️ Voice Settings")
lang_choice = st.sidebar.selectbox("Spoken Language", [
    "English (India)", "Telugu (తెలుగు)", "Hindi (हिंदी)", "Tamil (தமிழ்)", "Malayalam (മലയാളം)"
])
lang_map = {
    "English (India)": ("en-IN", "en-IN"),
    "Telugu (తెలుగు)": ("te-IN", "te-IN"),
    "Hindi (हिंदी)": ("hi-IN", "hi-IN"),
    "Tamil (தமிழ்)": ("ta-IN", "ta-IN"),
    "Malayalam (മലയാളം)": ("ml-IN", "ml-IN")
}
stt_code, tts_code = lang_map[lang_choice]

# API Keys setup
st.sidebar.markdown("---")
st.sidebar.subheader("🔑 API Setup (Required)")
groq_key = st.sidebar.text_input("Groq API Key (For Brain)", type="password", value=st.secrets.get("GROQ_API_KEY", ""))
hf_key = st.sidebar.text_input("Hugging Face Token (For Vision/Voice)", type="password", value=st.secrets.get("HUGGING_FACE_API_KEY", ""))

if not groq_key or not hf_key:
    st.sidebar.error("Please enter your API keys to unlock features.")

if mode == "💬 Voice & Chat (గళం)":
    st.header("Multilingual Alexa-Style Assistant")
    st.info("I am your local expert! Talk to me in slang, and I'll give you actionable 1-2-3 fixes.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        prompt_text = st.chat_input("Type your electrical problem here...")

    with col2:
        st.markdown(f"### 🎙️ Tap to Speak ({lang_choice})")
        audio_bytes = audio_recorder(text="Record", recording_color="#e83e8c", neutral_color="#4da6ff", icon_size="2x")

    user_text = ""
    
    if audio_bytes:
        # Check if the audio is just a 0.5s click (often under 20KB for this bitrate)
        if len(audio_bytes) < 30000:
            st.warning("⚠️ Recording too short. Please tap the mic, speak clearly, and tap again to stop.")
        else:
            with st.spinner("Processing Voice..."):
                recognized_text = voice_utils.process_audio_bytes(audio_bytes, hf_key=hf_key, lang_code=stt_code)
                if recognized_text and not recognized_text.startswith("Sorry") and not recognized_text.startswith("Error"):
                    user_text = recognized_text
                else:
                    st.error("Audio not clearly recognized. Please try again or check your microphone.")

    if prompt_text:
        user_text = prompt_text

    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        with col1:
            with st.chat_message("user"):
                st.markdown(user_text)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    chat_history = st.session_state.messages[-8:]
                    response = ai_engine.chat_with_electrician(chat_history, groq_key=groq_key, target_language=lang_choice)
                    st.markdown(response)
                    
                    # Alexa-style instant playback
                    js_audio = voice_utils.text_to_speech(response, lang=tts_code)
                    if js_audio:
                        html_audio = voice_utils.get_audio_html(js_audio)
                        st.components.v1.html(html_audio, height=0)

            st.session_state.messages.append({"role": "assistant", "content": response})

elif mode == "🔧 Dynamic Troubleshooter":
    st.header("Real-World Equipment Troubleshooter")
    st.info("Select your equipment and describe the exact issue. The AI will instantly generate a safe, step-by-step fix.")
    
    col1, col2 = st.columns(2)
    with col1:
        device = st.selectbox("1. Select Equipment", [
            "Single Phase Water Motor", "3-Phase Industrial Motor", 
            "Ceiling Fan", "Mixer Grinder", "Submersible Pump"
        ])
    with col2:
        problem = st.text_input("2. Describe Problem", placeholder="e.g. 'Humming noise and burning smell'")
        
    st.markdown("---")
    if problem and st.button("Generate Fix & Tools Required ⚡", use_container_width=True):
        with st.spinner(f"Diagnosing {device}..."):
            sys_prompt = f"Equipment: {device}. Problem: {problem}. Please give an exact Diagnosis, Tools Required, 1-2-3 Step-by-Step Fix, and exact Parts/Specs to Buy (Breakers, wire mm2, capacitor uF). Do not write introduction paragraphs."
            resp = ai_engine.chat_with_electrician([{"role": "user", "content": sys_prompt}], groq_key=groq_key, target_language=lang_choice)
            st.success("🤖 AI Diagnosis Complete")
            st.markdown(resp)

elif mode == "📹 Live Video / Scanner":
    st.header("Live Video / Nameplate Scanner")
    st.info("Take a quick snapshot from your device camera. The AI will extract Nameplate data or diagnose burnt components directly from the visual feed.")
    
    st.markdown("### 📸 Snapshot Capture")
    col1, col2 = st.columns(2)
    with col1:
        camera_img = st.camera_input("Take Live Snapshot")
    
    with col2:
        upload_img = st.file_uploader("Or Upload existing photo", type=["jpg", "png", "jpeg"])
        
    active_img = camera_img if camera_img else upload_img
    
    if active_img:
        st.image(active_img, width=400)
        custom_prompt = st.text_input("What should the AI look for?", value="Extract Voltage, Power (HP/kW), Current (FLA/Amps), Phase, RPM, and Frame Size. Or identify any physical damage.")
        if st.button("Analyze Image 🔍", use_container_width=True):
            with st.spinner("Analyzing high-definition visual feed..."):
                bytes_data = active_img.getvalue()
                b64_image = base64.b64encode(bytes_data).decode('utf-8')
                
                response = ai_engine.analyze_image(b64_image, custom_prompt, hf_key=hf_key)
                st.success("Analysis Complete!")
                st.markdown(response)

elif mode == "⚡ Load & Gauge Finder":
    st.header("Advanced Motor Load Analyzer & Gauge Finder")
    hp = st.number_input("Motor HP", min_value=0.1, max_value=1000.0, value=2.0, step=0.5)
    phase = st.selectbox("Phase", [1, 3])
    voltage = st.number_input("Voltage (V)", value=230 if phase==1 else 415, step=10)
    if st.button("Calculate Safety Parameters ⚡"):
        amps, breaker = calculators.calculate_motor_load(hp, phase, voltage)
        st.metric("Full Load Amperes", f"{amps} A")
        st.metric("Recommended Wire Size", f"{calculators.recommend_wire_size(amps)} mm²")
        st.success("Calculations are formulated with a 25% safety overhead for breaker sizing.")
        
    st.markdown("---")
    st.subheader("🎯 Starting and Ending Gauge Finder (Rewinding)")
    rw_hp = st.number_input("Motor HP for Rewinding", value=1.0, step=0.5)
    r_phase = st.selectbox("Motor Phase", [1, 3], key="rw_phase")
    if st.button("Find Gauge Specification"):
        with st.spinner("Calculating Standard Gauge..."):
            prompt = f"What is the exact standard starting gauge (SWG) and ending/running gauge (SWG) for rewinding a {rw_hp} HP {r_phase} Phase motor? List the gauge numbers."
            resp = ai_engine.chat_with_electrician([{"role": "user", "content": prompt}], groq_key=groq_key, target_language=lang_choice)
            st.info("Gauge Specifications Based on Standards:")
            st.markdown(resp)

elif mode == "📏 Circuit & Voltage Calculator":
    st.header("Voltage Drop Calculator")
    current = st.number_input("Load Current (Amps)", value=10.0)
    distance = st.number_input("Distance to Load (Meters)", value=30.0)
    wire = st.selectbox("Wire Size (mm²)", [1.5, 2.5, 4.0, 6.0, 10.0])
    if st.button("Analyze Drop"):
        vd, vend, pdrop, sf = calculators.calculate_voltage_drop(current, distance, wire, phase=1)
        st.write(f"Drop: {vd}V | Status: {sf}")

elif mode == "🛠️ Winding Database":
    st.header("Standard Winding Specs")
    cat = st.selectbox("Category", list(knowledge_base.WINDING_DATA.keys()))
    mod = st.selectbox("Model", list(knowledge_base.WINDING_DATA[cat].keys()))
    st.json(knowledge_base.WINDING_DATA[cat][mod])
