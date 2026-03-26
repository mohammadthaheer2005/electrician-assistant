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

# Hide API keys in frontend (Handled in backend files)
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
                recognized_text = voice_utils.process_audio_bytes(audio_bytes, lang_code=stt_code)
                if recognized_text and not recognized_text.startswith("Sorry") and not recognized_text.startswith("Error"):
                    user_text = recognized_text
                elif recognized_text and recognized_text.startswith("Error"):
                    st.error(f"Backend Server Error: {recognized_text}")
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
                    response = ai_engine.chat_with_electrician(chat_history, target_language=lang_choice)
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
            resp = ai_engine.chat_with_electrician([{"role": "user", "content": sys_prompt}], target_language=lang_choice)
            st.success("🤖 AI Diagnosis Complete")
            st.markdown(resp)

elif mode == "📹 Live Video / Scanner":
    st.header("🔴 Real-Time Video AI Assistant")
    st.info("Point your camera and ask the AI about any electrical component. Highly interactive visual diagnostics.")
    
    st.markdown("### 1. Enable Camera")
    camera_img = st.camera_input("Capture Frame for AI Analysis")
    
    if camera_img:
        st.session_state.last_vision_img = camera_img
        st.image(st.session_state.last_vision_img, width=400, caption="Current Snapshot")
        
    st.markdown("### 2. Voice/Text Question")
    v_col1, v_col2 = st.columns([2, 1])
    with v_col1:
        vision_prompt = st.text_input("Ask me anything about the photo above...", placeholder="e.g. 'Is this wire gauge correct?'", key="v_prompt")
    with v_col2:
        v_audio = audio_recorder(text="Talk to AI", icon_size="2x", key="v_audio")
        
    if v_audio and len(v_audio) > 30000:
        with st.spinner("Listening to your question..."):
            recognized_q = voice_utils.process_audio_bytes(v_audio, lang_code=stt_code)
            if recognized_q and not recognized_q.startswith("Error"):
                st.session_state.v_query = recognized_q
                st.info(f"You asked: {recognized_q}")
            else:
                st.error("Could not hear you. Try typing.")

    # Process if we have an image and a query (either text or voice)
    active_query = vision_prompt if vision_prompt else st.session_state.get("v_query")
    
    if active_query and st.session_state.get("last_vision_img"):
        if st.button("Start AI Call Analysis ⚡", use_container_width=True):
            with st.spinner("AI is analyzing the video frame..."):
                bytes_data = st.session_state.last_vision_img.getvalue()
                b64_image = base64.b64encode(bytes_data).decode('utf-8')
                
                combined_prompt = f"Context: Video Analysis. User Question: {active_query}. Extract exact technical details."
                response = ai_engine.analyze_image(b64_image, combined_prompt)
                st.success("Analysis Complete!")
                st.markdown(response)
                
                # Voice response
                js_audio = voice_utils.text_to_speech(response, lang=tts_code)
                if js_audio:
                    html_audio = voice_utils.get_audio_html(js_audio)
                    st.components.v1.html(html_audio, height=0)

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
            resp = ai_engine.chat_with_electrician([{"role": "user", "content": prompt}], target_language=lang_choice)
            st.info("Gauge Specifications Based on Standards:")
            st.markdown(resp)

elif mode == "📏 Circuit Voltage Drop":
    st.header("Voltage Drop Calculator")
    st.info("Ensure wire lengths won't cause dangerous electrical undervoltage.")
    current = st.number_input("Load Current (Amps)", value=10.0, step=1.0)
    distance = st.number_input("Distance to Load (Meters)", value=30.0, step=5.0)
    wire = st.selectbox("Wire Size (mm²)", [1.5, 2.5, 4.0, 6.0, 10.0, 16.0, 25.0])
    if st.button("Analyze Drop"):
        vd, vend, pdrop, sf = calculators.calculate_voltage_drop(current, distance, wire, phase=1)
        st.metric("Voltage Drop", f"{vd}V ({pdrop}%)")
        st.success(f"Final Voltage: {vend}V | Status: {sf}")

elif mode == "🛠️ Winding Database":
    st.header("Standard Winding Specs")
    cat = st.selectbox("Category", list(knowledge_base.WINDING_DATA.keys()))
    mod = st.selectbox("Model", list(knowledge_base.WINDING_DATA[cat].keys()))
    st.json(knowledge_base.WINDING_DATA[cat][mod])
