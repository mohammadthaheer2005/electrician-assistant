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
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=120)
st.sidebar.title("⚙️ Command Center")
mode = st.sidebar.radio("Navigation:", [
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
    "English (India)", "Telugu (తెలుగు)", "Hindi (हिंदी)", "Tamil (தமிழ்)", "Malayalam (മലയാളం)"
])
lang_map = {
    "English (India)": ("en-IN", "en-IN"),
    "Telugu (తెలుగు)": ("te-IN", "te-IN"),
    "Hindi (हिंदी)": ("hi-IN", "hi-IN"),
    "Tamil (தமிழ்)": ("ta-IN", "ta-IN"),
    "Malayalam (മലയാളం)": ("ml-IN", "ml-IN")
}
stt_code, tts_code = lang_map[lang_choice]

if mode == "💬 Voice & Chat (గళం)":
    st.header("Multilingual Alexa-Style Assistant")
    st.info("Instant Voice Recognition: Tap the mic and start talking! No server delay.")
    
    # -- BROWSER NATIVE STT COMPONENT --
    st.components.v1.html(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <button id="stt-btn" style="
                background: linear-gradient(135deg, #2563EB, #1E40AF);
                color: white; border: none; padding: 15px 40px; 
                border-radius: 50px; font-weight: bold; cursor: pointer;
                box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
                display: flex; align-items: center; gap: 12px; font-family: 'Inter', sans-serif;
                font-size: 16px; transition: all 0.2s ease;
            ">
                <span id="mic-icon">🎙️</span>
                <span id="btn-text">Tap to Speak</span>
            </button>
        </div>
        <script>
            const btn = document.getElementById('stt-btn');
            const icon = document.getElementById('mic-icon');
            const text = document.getElementById('btn-text');
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

            if (!SpeechRecognition) {{
                text.innerText = "Error: Browser not supported";
                btn.style.opacity = "0.5";
            }} else {{
                const recognition = new SpeechRecognition();
                recognition.lang = '{stt_code}';
                recognition.onstart = () => {{
                    text.innerText = "Listening...";
                    icon.innerText = "🛑";
                    btn.style.background = "linear-gradient(135deg, #EF4444, #B91C1C)";
                }};
                recognition.onresult = (e) => {{
                    const val = e.results[0][0].transcript;
                    window.parent.postMessage({{
                        type: 'streamlit:set_widget_value',
                        data: {{ id: 'chat_input_voice', value: val }}
                    }}, '*');
                }};
                recognition.onend = () => {{
                    text.innerText = "Tap to Speak";
                    icon.innerText = "🎙️";
                    btn.style.background = "linear-gradient(135deg, #2563EB, #1E40AF)";
                }};
                btn.onclick = () => recognition.start();
            }}
        </script>
    """, height=100)

    # Use a hidden text input to catch the voice result
    voice_transcript = st.text_input("Voice Catch", key="chat_input_voice", label_visibility="collapsed")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_col, dummy_col = st.columns([4, 1])
    with chat_col:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        prompt_text = st.chat_input("Type or use Voice button above...")

    # Logic: If we have voice_transcript or prompt_text, process it.
    user_text = prompt_text if prompt_text else voice_transcript

    if user_text:
        # Clear the voice catch to avoid loops
        if user_text == voice_transcript:
            st.session_state.chat_input_voice = ""
            
        st.session_state.messages.append({"role": "user", "content": user_text})
        with chat_col:
            # We don't need to manually write user message here, st.rerun will handle it via state
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    chat_history = st.session_state.messages[-8:]
                    response = ai_engine.chat_with_electrician(chat_history, target_language=lang_choice)
                    st.markdown(response)
                    js_audio = voice_utils.text_to_speech(response, lang=tts_code)
                    if js_audio:
                        st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

elif mode == "🔧 Dynamic Troubleshooter":
    st.header("Real-World Equipment Troubleshooter")
    st.info("Select equipment and issue for 1-2-3 fixes.")
    c1, c2 = st.columns(2)
    with c1: device = st.selectbox("Device", ["Fan", "Motor", "Pump", "Mixer", "DB Board"])
    with c2: problem = st.text_input("Issue", placeholder="e.g. 'Humming noise'")
    if problem and st.button("Generate Fix"):
        with st.spinner("Diagnosing..."):
            p = f"Equipment: {device}. Problem: {problem}. diagnosis, tools, 1-2-3 fix."
            st.markdown(ai_engine.chat_with_electrician([{"role":"user","content":p}], target_language=lang_choice))

elif mode == "📹 Live Video / Scanner":
    st.header("🔴 Real-Time Video AI Assistant")
    st.info("You can now either capture a live frame OR upload an existing component photo for analysis.")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        camera_img = st.camera_input("Capture Live Frame")
    with col_v2:
        upload_img = st.file_uploader("Upload Component Photo", type=["jpg", "png", "jpeg"])
    
    active_img = camera_img if camera_img else upload_img
    
    if active_img:
        st.image(active_img, width=400, caption="Analyzing this component...")
        st.session_state.last_vision_img = active_img
        
        v_col1, v_col2 = st.columns([2, 1])
        with v_col1: prompt = st.text_input("Ask about this photo...", key="v_p")
        with v_col2: v_audio = audio_recorder(text="Ask via Voice", key="v_a")
        
        q_text = prompt
        if v_audio and len(v_audio) > 30000:
            with st.spinner("Listening..."):
                q = voice_utils.process_audio_bytes(v_audio, lang_code=stt_code)
                if q and not q.startswith("Error"): q_text = q
        
        if q_text and st.button("Analyze Current View 🔍"):
            with st.spinner("AI Analysis..."):
                b64 = base64.b64encode(st.session_state.last_vision_img.getvalue()).decode('utf-8')
                resp = ai_engine.analyze_image(b64, q_text)
                st.success("Analysis Complete!")
                st.markdown(resp)
                js_audio = voice_utils.text_to_speech(resp, lang=tts_code)
                if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)

elif mode == "⚡ Load & Gauge Finder":
    st.header("Motor Load & Rewinding Spec Finder")
    hp = st.number_input("HP", value=1.0)
    phases = st.selectbox("Phase", [1, 3])
    if st.button("Calc Load"):
        amps, brk = calculators.calculate_motor_load(hp, phases, 230 if phases==1 else 415)
        st.metric("Load Amps", f"{amps}A")
        st.metric("Wire", f"{calculators.recommend_wire_size(amps)}mm²")
    st.markdown("---")
    st.subheader("🎯 REWINDING GAUGE FINDER")
    if st.button("Find Exact SWG Specs (Starting & Running)"):
        with st.spinner("Calculating Standard Gauge..."):
            p = f"What is the exact standard STARTING/START GAUGE (SWG) and RUNNING/RUN GAUGE (SWG) for rewinding a {hp} HP {phases} Phase motor? Respond with a clear markdown table showing: | Parameter | SWG Value |."
            st.markdown(ai_engine.chat_with_electrician([{"role":"user","content":p}], target_language=lang_choice))

elif mode == "📏 Circuit Voltage Drop":
    st.header("Voltage Drop Analysis")
    dist = st.number_input("Distance (Meters)", value=30)
    wire = st.selectbox("Wire (mm²)", [1.5, 2.5, 4.0, 6.0])
    if st.button("Calculate Drop"):
        vd, vend, pd, sf = calculators.calculate_voltage_drop(10, dist, wire)
        st.metric("Drop", f"{vd}V")
        st.success(f"Status: {sf}")

elif mode == "🛠️ Winding Database":
    st.header("Local Model Winding Database")
    cat = st.selectbox("DB Category", list(knowledge_base.WINDING_DATA.keys()))
    mod = st.selectbox("DB Model", list(knowledge_base.WINDING_DATA[cat].keys()))
    st.json(knowledge_base.WINDING_DATA[cat][mod])

