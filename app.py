import streamlit as st
from audio_recorder_streamlit import audio_recorder
import ai_engine
import voice_utils
import calculators
import knowledge_base

st.set_page_config(page_title="ElectroAssist AI", page_icon="⚡", layout="wide")

st.title("⚡ Electrician Smart Assistant")
st.markdown("Your interactive, Alexa-like helper for electrical troubleshooting and calculations.")

# Sidebar Navigation
mode = st.sidebar.radio("Navigation", ["💬 Chat & Voice Assistant", "⚡ Motor Load Analyzer", "📏 Wire & Voltage Calculator", "🛠️ Winding Helber DB"])

if mode == "💬 Chat & Voice Assistant":
    st.header("Multilingual Voice & Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Voice Input (Alexa-like experience)
    st.markdown("### 🎙️ Tap to Speak")
    audio_bytes = audio_recorder(text="Click to Record", recording_color="#e83e8c", neutral_color="#ffffff", icon_size="2x")
    
    user_text = ""
    
    if audio_bytes:
        with st.spinner("Transcribing audio..."):
            recognized_text = voice_utils.process_audio_bytes(audio_bytes)
            if recognized_text and not recognized_text.startswith("Sorry") and not recognized_text.startswith("Error"):
                user_text = recognized_text
                st.success(f"Heard: {user_text}")
            else:
                st.error(recognized_text)

    # Text Input fallback
    prompt_text = st.chat_input("Or type your electrical question here...")
    
    if prompt_text:
        user_text = prompt_text

    if user_text:
        # Add to state and display
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # limit history to last 10 messages to save tokens
                chat_history = st.session_state.messages[-10:]
                
                response = ai_engine.chat_with_electrician(chat_history)
                st.markdown(response)
                
                # Convert response to Voice (Alexa functionality)
                b64_audio = voice_utils.text_to_speech(response)
                if b64_audio:
                    html_audio = voice_utils.get_audio_html(b64_audio)
                    st.components.v1.html(html_audio, height=0)

        st.session_state.messages.append({"role": "assistant", "content": response})

elif mode == "⚡ Motor Load Analyzer":
    st.header("Motor Load Analyzer")
    hp = st.number_input("Motor HP", min_value=0.1, max_value=500.0, value=2.0)
    phase = st.selectbox("Phase", [1, 3])
    voltage = st.number_input("Voltage (V)", value=230 if phase==1 else 415)
    
    if st.button("Calculate"):
        amps, breaker = calculators.calculate_motor_load(hp, phase, voltage)
        wire_size = calculators.recommend_wire_size(amps)
        st.success(f"**Full Load Amperes (FLA):** {amps} A")
        st.info(f"**Recommended Breaker Size:** {breaker} A")
        st.warning(f"**Minimum Wire Size:** {wire_size} mm²")

elif mode == "📏 Wire & Voltage Calculator":
    st.header("Wire Gauge & Voltage Drop Calculator")
    current = st.number_input("Current (Amps)", value=10.0)
    distance = st.number_input("Distance (Meters)", value=30.0)
    wire_size = st.selectbox("Wire Size (mm²)", [1.0, 1.5, 2.5, 4.0, 6.0, 10.0, 16.0, 25.0, 35.0])
    phase = st.selectbox("Phase", [1, 3])
    
    if st.button("Analyze Drop"):
        vd, v_end, p_drop, safety = calculators.calculate_voltage_drop(current, distance, wire_size, phase=phase)
        st.write(f"**Voltage Drop:** {vd} V")
        st.write(f"**Voltage at Load:** {v_end} V")
        st.write(f"**Percentage Drop:** {p_drop} %")
        if safety == "Safe":
            st.success("Safety Status: SAFE (<= 5% drop)")
        else:
            st.error("Safety Status: UNSAFE (> 5% drop)")

elif mode == "🛠️ Winding Helber DB":
    st.header("Winding Information Database")
    category = st.selectbox("Select Category", list(knowledge_base.WINDING_DATA.keys()))
    item = st.selectbox("Select Model", list(knowledge_base.WINDING_DATA[category].keys()))
    
    st.json(knowledge_base.WINDING_DATA[category][item])
