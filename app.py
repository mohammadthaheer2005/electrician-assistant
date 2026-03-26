import streamlit as st
from audio_recorder_streamlit import audio_recorder
import ai_engine
import voice_utils
import calculators
import knowledge_base
import base64

st.set_page_config(page_title="ElectroAssist AI", page_icon="⚡", layout="wide")

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
mode = st.sidebar.radio("Go to:", ["💬 AI Chat & Vision (గళం/Voice)", "⚡ Motor Load Analyzer", "📏 Circuit & Voltage Calculator", "🛠️ Winding Database"])

# Language Configuration for Voice
st.sidebar.markdown("---")
st.sidebar.subheader("🗣️ Voice Settings")
lang_choice = st.sidebar.selectbox("Spoken Language", [
    "English (India)", "Telugu (తెలుగు)", "Hindi (हिंदी)", "Tamil (தமிழ்)", "Malayalam (മലയാളം)"
])
lang_map = {
    "English (India)": ("en-IN", "en"),
    "Telugu (తెలుగు)": ("te-IN", "te"),
    "Hindi (हिंदी)": ("hi-IN", "hi"),
    "Tamil (தமிழ்)": ("ta-IN", "ta"),
    "Malayalam (മലയാളം)": ("ml-IN", "ml")
}
stt_code, tts_code = lang_map[lang_choice]

if mode == "💬 AI Chat & Vision (గళం/Voice)":
    st.header("Multilingual AI & Vision Diagnostics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        # Text Input
        prompt_text = st.chat_input("Type your electrical problem here...")

    with col2:
        st.markdown(f"### 🎙️ Tap to Speak ({lang_choice})")
        audio_bytes = audio_recorder(text="Record", recording_color="#e83e8c", neutral_color="#4da6ff", icon_size="2x")
        
        st.markdown("---")
        st.markdown("### 📸 Vision Upload")
        st.markdown("Upload a photo of a burnt motor, panel, or circuit for AI inspection.")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Image for Analysis", use_container_width=True)

    user_text = ""
    vision_mode = False
    
    # Process Voice Input
    if audio_bytes:
        with st.spinner("Processing Voice..."):
            recognized_text = voice_utils.process_audio_bytes(audio_bytes, lang_code=stt_code)
            if recognized_text and not recognized_text.startswith("Sorry") and not recognized_text.startswith("Error"):
                user_text = recognized_text
            else:
                st.error("Audio not clearly recognized. Please try again.")

    # Process Text Input
    if prompt_text:
        user_text = prompt_text

    # Action Trigger
    if user_text or (uploaded_file and st.button("Inspect Image 🔍")):
        if uploaded_file and not user_text:
            user_text = "Please examine this electrical component and identify any visible issues or standard specifications."
            vision_mode = True
        elif uploaded_file and user_text:
            vision_mode = True

        st.session_state.messages.append({"role": "user", "content": f"{'[Photo Attached] ' if vision_mode else ''}{user_text}"})
        
        with col1:
            with st.chat_message("user"):
                st.markdown(user_text)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    if vision_mode:
                        # Convert image to base64
                        bytes_data = uploaded_file.getvalue()
                        b64_image = base64.b64encode(bytes_data).decode('utf-8')
                        response = ai_engine.analyze_image(b64_image, user_text)
                    else:
                        chat_history = st.session_state.messages[-8:]
                        # Request AI to reply in the user's chosen local language
                        response = ai_engine.chat_with_electrician(chat_history, target_language=lang_choice)
                    
                    st.markdown(response)
                    
                    # Convert response to Voice automatically
                    b64_audio = voice_utils.text_to_speech(response, lang=tts_code)
                    if b64_audio:
                        html_audio = voice_utils.get_audio_html(b64_audio)
                        st.components.v1.html(html_audio, height=0)

            st.session_state.messages.append({"role": "assistant", "content": response})

elif mode == "⚡ Motor Load Analyzer":
    st.header("Advanced Motor Load Analyzer")
    st.info("Input your motor specifications to generate safe current ratings and cable sizing based on Standard Ampacity guidelines.")
    
    colA, colB, colC = st.columns(3)
    with colA:
        hp = st.number_input("Motor HP", min_value=0.1, max_value=1000.0, value=2.0, step=0.5)
    with colB:
        phase = st.selectbox("Phase", [1, 3])
    with colC:
        voltage = st.number_input("Voltage (V)", value=230 if phase==1 else 415, step=10)
        
    st.markdown("---")
    
    if st.button("Calculate Safety Parameters ⚡", use_container_width=True):
        amps, breaker = calculators.calculate_motor_load(hp, phase, voltage)
        wire_size = calculators.recommend_wire_size(amps)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Full Load Amperes (FLA)", f"{amps} A")
        m2.metric("Recommended Breaker", f"{breaker} A")
        m3.metric("Min. Copper Wire", f"{wire_size} mm²")
        st.success("Calculations are formulated with a 25% safety overhead for breaker sizing.")

elif mode == "📏 Circuit & Voltage Calculator":
    st.header("Precision Distance & Voltage Calculator")
    st.info("Ensure your long-distance pump/fan runs without burning out due to low voltage.")
    
    cA, cB = st.columns(2)
    with cA:
        current = st.number_input("Current (Amps) load", value=10.0)
        distance = st.number_input("Distance to Motor (Meters)", value=30.0)
    with cB:
        wire_size = st.selectbox("Wire Gauge Used (mm²)", [1.0, 1.5, 2.5, 4.0, 6.0, 10.0, 16.0, 25.0, 35.0])
        phase = st.selectbox("Phase Selection", [1, 3])
        
    st.markdown("---")
    if st.button("Analyze Cable Viability", use_container_width=True):
        vd, v_end, p_drop, safety = calculators.calculate_voltage_drop(current, distance, wire_size, phase=phase)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Voltage Drop", f"{vd} V")
        m2.metric("Terminal Voltage", f"{v_end} V")
        m3.metric("Percentage Drop", f"{p_drop} %")
        
        if safety == "Safe":
            st.success("✅ Cable is Safe. Voltage drop is within the 5% tolerance limit.")
        else:
            st.error("⚠️ UNSAFE. Voltage drop exceeds 5%. The motor will overheat. Please use a thicker wire gauge.")

elif mode == "🛠️ Winding Database":
    st.header("Standard Master Winding Reference")
    st.info("Select a device category to view Standard Indian specification data for Rewinding.")
    
    category = st.selectbox("Select Equipment Type", list(knowledge_base.WINDING_DATA.keys()))
    item = st.selectbox("Select Specific Model", list(knowledge_base.WINDING_DATA[category].keys()))
    
    data = knowledge_base.WINDING_DATA[category][item]
    
    st.markdown("### Internal Specifications")
    for key, val in data.items():
        if isinstance(val, list):
            st.markdown(f"**{key.replace('_', ' ').title()}:**")
            for bullet in val:
                st.markdown(f"- {bullet}")
        else:
            st.markdown(f"**{key.replace('_', ' ').title()}:** {val}")
