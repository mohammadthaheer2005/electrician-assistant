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
    "🔧 Step-by-Step Troubleshooter",
    "📸 Motor Nameplate Scanner",
    "⚡ Motor Load Analyzer", 
    "📏 Circuit & Voltage Calculator", 
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
        with st.spinner("Processing Voice..."):
            recognized_text = voice_utils.process_audio_bytes(audio_bytes, lang_code=stt_code)
            if recognized_text and not recognized_text.startswith("Sorry") and not recognized_text.startswith("Error"):
                user_text = recognized_text
            else:
                st.error("Audio not clearly recognized. Please try again.")

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

elif mode == "🔧 Step-by-Step Troubleshooter":
    st.header("Real-World Equipment Troubleshooter")
    st.info("A rule-based AI diagnostic flow exactly like a master technician.")
    
    device = st.selectbox("1. Select Equipment", ["Single Phase Water Motor", "Ceiling Fan", "Mixer Grinder"])
    
    if device == "Single Phase Water Motor":
        problem = st.selectbox("2. Select Problem Component", ["Motor humming but not turning", "Motor completely dead", "Overheating/Burning smell", "Low Speed / Low Water Pressure"])
        st.markdown("---")
        
        if problem == "Motor humming but not turning":
            st.subheader("🤖 AI Diagnosis")
            st.error("**Likely Cause:** Starting Capacitor Failure or Centrifugal Switch Stuck")
            st.markdown("""
            **🛠 Tools Required:** Multimeter, Screwdriver, Insulated Pliers.
            
            **Step-by-Step Fix:**
            1. **Turn OFF Main Power (Breaker).** Verify 0V with Multimeter.
            2. Open the terminal box and inspect the capacitor. Look for bulging or leaks.
            3. Spin the motor shaft by hand. If it rotates freely, the capacitor is dead.
            4. Remove capacitor, discharge it across pins with an insulated screwdriver.
            
            **🛍️ What You Need to Buy:**
            👉 Standard Run Capacitor for 1HP: **10µF - 15µF / 440V AC**
            👉 Standard Run Capacitor for 2HP: **20µF - 25µF / 440V AC**
            """)
        elif problem == "Motor completely dead":
            st.subheader("🤖 AI Diagnosis")
            st.warning("**Likely Cause:** No Supply Voltage or Internal Winding Open")
            st.markdown("""
            **🛠 Tools Required:** Multimeter/Clamp Meter.
            
            **Step-by-Step Fix:**
            1. Measure voltage at the motor terminals. Should be ~230V.
            2. If 0V, check the incoming breaker/overload relay switch.
            3. If voltage is present, disconnect power and measure coil continuity (Running & Starting coils).
            4. If coils read Open (OL), winding is burnt. Send for rewinding.
            
            **🛍️ What You Need to Buy:**
            👉 If overload relay failed: **Thermal Overload Relay (Match Motor FLA rating)**
            """)
            
    elif device == "Ceiling Fan":
        problem = st.selectbox("2. Select Problem Component", ["Fan not rotating (Just humming)", "Slow speed", "Wobbling / Noise"])
        st.markdown("---")
        if problem == "Fan not rotating (Just humming)":
            st.subheader("🤖 AI Diagnosis")
            st.error("**Likely Cause:** Dead Capacitor or Jammed Ball Bearings")
            st.markdown("""
            **🛠 Tools Required:** Tester, Insulated Screwdriver, Spanner.
            
            **Step-by-Step Fix:**
            1. **Turn OFF switch (and fan regulator).**
            2. Try spinning fan manually. If stiff, bearings (6201/6202 size) need replacement.
            3. If free, uncap the top canopy and check the black box (capacitor).
            4. Replace it.
            
            **🛍️ What You Need to Buy:**
            👉 New Fan Capacitor: **2.5µF (Standard) or 3.15µF (If old fan winding is weak)**
            👉 Replacement Bearings (if tight): **6201ZZ or 6202ZZ series**
            """)

elif mode == "📸 Motor Nameplate Scanner":
    st.header("Motor Nameplate OCR Scanner")
    st.info("Point your camera at a motor's sticker plate. The AI will extract exact data to verify load and components.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Take a LIVE photo:")
        camera_img = st.camera_input("Scanner")
    
    with col2:
        st.write("Or Upload existing photo:")
        upload_img = st.file_uploader("Nameplate File", type=["jpg", "png", "jpeg"])
        
    active_img = camera_img if camera_img else upload_img
    
    if active_img:
        st.image(active_img, width=400)
        if st.button("Scan Nameplate 🔍", use_container_width=True):
            with st.spinner("Analyzing Nameplate Specifications..."):
                bytes_data = active_img.getvalue()
                b64_image = base64.b64encode(bytes_data).decode('utf-8')
                
                custom_prompt = """
                Extract specific data from this motor nameplate. List clearly:
                - Voltage (V)
                - Power (HP or kW)
                - Current (FLA / Amps)
                - Phase
                - RPM
                - Frame Size
                If you cannot see it clearly, explain what is missing.
                """
                response = ai_engine.analyze_image(b64_image, custom_prompt)
                st.success("Analysis Complete!")
                st.markdown(response)

elif mode == "⚡ Motor Load Analyzer":
    st.header("Advanced Motor Load Analyzer")
    hp = st.number_input("Motor HP", min_value=0.1, max_value=1000.0, value=2.0, step=0.5)
    phase = st.selectbox("Phase", [1, 3])
    voltage = st.number_input("Voltage (V)", value=230 if phase==1 else 415, step=10)
    if st.button("Calculate Safety Parameters ⚡"):
        amps, breaker = calculators.calculate_motor_load(hp, phase, voltage)
        st.metric("Full Load Amperes", f"{amps} A")
        st.metric("Recommended Wire Size", f"{calculators.recommend_wire_size(amps)} mm²")

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
