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
# Single Unified Dashboard
st.header("🔴 Multi-Modal Smart Assistant")
st.info("Point your camera, upload a photo, or talk to me! I can see what you see and solve any electrical problem.")

# 1. Vision Assistant (Priority)
st.markdown("### 📸 Vision & Camera Analysis")
camera_img = st.camera_input("Capture Live Frame")
upload_img = st.file_uploader("Or Upload Component Photo", type=["jpg", "png", "jpeg"])
active_img = camera_img if camera_img else upload_img

if active_img:
    st.session_state.last_vision_img = active_img
    st.image(active_img, width=400, caption="Analyzing this component...")
    
v_col1, v_col2 = st.columns([2, 1])
with v_col1:
    vision_prompt = st.text_input("Ask me about the photo...", placeholder="e.g. 'Read this nameplate' or 'Is this capacitor burnt?'", key="v_prompt")
with v_col2:
    v_audio = audio_recorder(text="Ask by Voice", icon_size="2x", key="v_audio_main")

if v_audio and len(v_audio) > 30000:
    with st.spinner("Listening..."):
        q = voice_utils.process_audio_bytes(v_audio, lang_code=stt_code)
        if q and not q.startswith("Error"):
            st.session_state.v_query = q
            st.info(f"Hearing: {q}")

active_query = vision_prompt if vision_prompt else st.session_state.get("v_query")
if active_query and st.session_state.get("last_vision_img"):
    if st.button("Analyze Current View 🔍", use_container_width=True):
        with st.spinner("AI is examining the image..."):
            b64_image = base64.b64encode(st.session_state.last_vision_img.getvalue()).decode('utf-8')
            resp = ai_engine.analyze_image(b64_image, active_query)
            st.success("Analysis Complete!")
            st.markdown(resp)
            js_audio = voice_utils.text_to_speech(resp, lang=tts_code)
            if js_audio:
                st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)

st.markdown("---")

# 2. Interactive Chat & Diagnosis
with st.expander("💬 Voice Chat & Problem Diagnosis", expanded=False):
    st.subheader("Alexa-Style Field Assistant")
    c1, c2 = st.columns([3, 1])
    with c1:
        if "messages" not in st.session_state: st.session_state.messages = []
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])
        chat_in = st.chat_input("Diagnose a general problem...")
    with c2:
        chat_audio = audio_recorder(text="Tap to Talk", icon_size="2.5x", key="chat_voice")
    
    u_text = chat_in
    if chat_audio and len(chat_audio) > 30000:
        recognized = voice_utils.process_audio_bytes(chat_audio, lang_code=stt_code)
        if recognized and not recognized.startswith("Error"): u_text = recognized

    if u_text:
        st.session_state.messages.append({"role": "user", "content": u_text})
        with st.spinner("Consulting field manuals..."):
            resp = ai_engine.chat_with_electrician(st.session_state.messages[-5:], target_language=lang_choice)
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.rerun()

# 3. Calculators & Database
with st.expander("⚡ Load, Gauge & Voltage Tools", expanded=False):
    tabs = st.tabs(["Load Analyzer", "Gauge Finder", "Voltage Drop", "Winding DB"])
    
    with tabs[0]:
        hp = st.number_input("Motor HP", value=2.0)
        ph = st.selectbox("Phase", [1, 3])
        if st.button("Run Load Check"):
            amps, breaker = calculators.calculate_motor_load(hp, ph, 230 if ph==1 else 415)
            st.metric("Amps", f"{amps}A")
            st.metric("Wire", f"{calculators.recommend_wire_size(amps)}mm²")
            
    with tabs[1]:
        ghp = st.number_input("HP for Rewinding", value=1.0)
        if st.button("Get SWG Specs"):
            p = f"Standard SWG gauges for {ghp} HP motor?"
            st.markdown(ai_engine.chat_with_electrician([{"role":"user","content":p}], target_language=lang_choice))

    with tabs[2]:
        dist = st.number_input("Meters", value=30)
        if st.button("Check Drop"):
            vd, vend, pd, sf = calculators.calculate_voltage_drop(10, dist, 2.5)
            st.metric("Drop", f"{vd}V")

    with tabs[3]:
        cat = st.selectbox("DB Category", list(knowledge_base.WINDING_DATA.keys()))
        mod = st.selectbox("DB Model", list(knowledge_base.WINDING_DATA[cat].keys()))
        st.json(knowledge_base.WINDING_DATA[cat][mod])

