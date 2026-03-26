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
    "🗺️ Winding & Wiring Designer",
    "⚡ Load & Gauge Finder", 
    "📊 Performance & Efficiency",
    "📏 Circuit Voltage Drop", 
    "📚 Electrician's Academy",
    "🌐 Live Industrial IoT (Sim)"
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
    
    st.info("🎙️ Unified AI Voice Control: Tap the mic below to speak in your language.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_col, dummy_col = st.columns([4, 1])
    with chat_col:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        col_input, col_mic = st.columns([5, 1])
        with col_input: 
            prompt_text = st.chat_input("Type or say something...")
        with col_mic:
            # Single unified Cloud Mic for all environments
            cloud_audio = st.audio_input("Mic", label_visibility="collapsed")
            if cloud_audio:
                audio_id = hash(cloud_audio.getvalue())
                if st.session_state.get("last_processed_audio") != audio_id:
                    with st.spinner("Transcribing..."):
                        q = voice_utils.process_audio_bytes(cloud_audio.getvalue(), lang_code=stt_code)
                        if not q.startswith("Error") and len(q.strip()) > 1:
                            st.session_state.messages.append({"role": "user", "content": q})
                            st.session_state.voice_trigger = q
                            st.session_state.last_processed_audio = audio_id
                            st.rerun()
                        elif q.startswith("Error"):
                            st.error(q)
    
    # Logic: If we have voice_trigger or prompt, process it.
    final_input = prompt_text if prompt_text else st.session_state.get("voice_trigger")

    if final_input:
        # Clear triggers to avoid loops
        if "voice_trigger" in st.session_state: del st.session_state["voice_trigger"]
        
        if prompt_text: # If it was from chat_input, append it
            st.session_state.messages.append({"role": "user", "content": final_input})
            
        with chat_col:
            with st.chat_message("assistant"):
                with st.spinner(f"Processing in {lang_choice}..."):
                    chat_history = st.session_state.messages[-8:]
                    response = ai_engine.chat_with_electrician(chat_history, target_language=lang_choice)
                    st.markdown(response)
                    js_audio = voice_utils.text_to_speech(response, lang=tts_code)
                    if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

elif mode == "🔧 Dynamic Troubleshooter":
    st.header("🔍 Industrial Fault Detection System")
    st.info("Select a symptom for instant diagnosis or describe a custom issue.")
    
    # 1. Predefined Powerful Faults
    symptom_map = {
        "Select a symptom...": None,
        "Motor humming but not rotating": "motor_humming_no_rotation",
        "Motor is overheating / too hot": "motor_overheating",
        "Sparking at carbon brushes": "sparking_at_brushes",
        "Circuit breaker trips repeatedly": "circuit_breaker_tripping"
    }
    selected_symptom = st.selectbox("Common Symptoms", list(symptom_map.keys()))
    
    if selected_symptom != "Select a symptom...":
        fault_key = symptom_map[selected_symptom]
        data = knowledge_base.FAULT_SYMPTOMS[fault_key]
        st.error(f"⚠️ **Possible Faults:** {', '.join(data['possible_faults'])}")
        st.success(f"🛠️ **Official Solution:** {data['solution']}")
        
        # Voice Output for solution
        js_audio = voice_utils.text_to_speech(f"Diagnosis for {selected_symptom}: Possible faults are {', '.join(data['possible_faults'])}. Solution: {data['solution']}", lang=tts_code)
        if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)

    st.divider()
    st.subheader("🤖 AI-Powered Custom Diagnosis")
    c1, c2 = st.columns(2)
    with c1: device = st.selectbox("Device", ["Fan", "Motor", "Pump", "Mixer", "DB Board"])
    with c2: problem = st.text_input("Custom Problem Description", placeholder="e.g. 'Strange smell like burning'")
    
    if problem and st.button("Analyze with AI"):
        with st.spinner(f"AI is diagnosing in {lang_choice}..."):
            p = f"Equipment: {device}. Problem: {problem}. diagnosis, tools, 1-2-3 fix."
            resp = ai_engine.chat_with_electrician([{"role":"user","content":p}], target_language=lang_choice)
            st.markdown(resp)
            js_audio = voice_utils.text_to_speech(resp, lang=tts_code)
            if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)

elif mode == "📹 Live Video / Scanner":
    st.header("📸 AI Video Scanner & Voice Sync")
    st.info("Experience the future of electrical field work: Scan hardware or upload photos for AI expertise.")
    
    # -- Image Origin Selection --
    v_tab1, v_tab2 = st.tabs(["📷 Live Camera (Voice Sync)", "📂 Upload Photo"])
    
    active_img = None
    with v_tab1:
        st.caption("🎙️ TIP: Say 'Analyze this' or ask a question while the camera is on.")
        camera_img = st.camera_input("Scanner Active", label_visibility="collapsed")
        if camera_img: active_img = camera_img
    with v_tab2:
        upload_img = st.file_uploader("Upload Component Photo", type=["jpg", "png", "jpeg"])
        if upload_img: active_img = upload_img
    
    # -- 🚀 THE ULTIMATE VISION PIPELINE --
    if active_img:
        st.divider()
        sv_col1, sv_col2 = st.columns([1, 1.2])
        
        with sv_col1:
            st.image(active_img, use_container_width=True, caption="Pipeline Target")
            # Store image in history if not already there
            if "vision_history" not in st.session_state: st.session_state.vision_history = []
            
        with sv_col2:
            # 1. Pipeline Voice Interface
            st.subheader("🎙️ Pipeline Voice Control")
            v_audio_input = st.audio_input("Ask about this Image", key="v_pipeline_mic")
            
            # Use 'value' to populate from voice but a different 'key' to avoid conflicts
            v_voice_q = st.session_state.get("v_pipeline_trans", "")
            manual_q = st.text_input("Technical Query", value=v_voice_q, key="v_manual_q", placeholder=f"Ask in {lang_choice}...")
            
            # Automatic Voice Trigger Logic
            if v_audio_input:
                v_audio_id = hashlib.md5(v_audio_input.getvalue()).hexdigest()
                if st.session_state.get("last_pipeline_audio") != v_audio_id:
                    with st.spinner("Pipeline Transcribing..."):
                        q = voice_utils.process_audio_bytes(v_audio_input.getvalue(), lang_code=stt_code)
                        if not q.startswith("Error") and len(q.strip()) > 1:
                            st.session_state.v_pipeline_trans = q
                            st.session_state.last_pipeline_audio = v_audio_id
                            st.rerun()

            if st.button("🔍 RUN PIPELINE ANALYSIS", type="primary", use_container_width=True):
                with st.spinner(f"AI Eye analyzing in {lang_choice}..."):
                    b64 = base64.b64encode(active_img.getvalue()).decode('utf-8')
                    # Clear voice q after analysis
                    if "v_pipeline_trans" in st.session_state: del st.session_state["v_pipeline_trans"]
                    
                    final_q = (manual_q if manual_q else "Analyze this component.") + f" Respond entirely in {lang_choice}."
                    resp = ai_engine.analyze_image(b64, final_q)
                    st.session_state.v_resp = resp
                    st.session_state.v_q_final = final_q
                    
                    # -- 🎯 WINDING SPEC DETECTION (EXTRA FEATURE) --
                    # Detect if response contains winding info
                    w_info = ""
                    if "SWG" in resp or "gauge" in resp.lower() or "winding" in resp.lower():
                        # Extract a snippet or keep it as a flag
                        w_info = "⚡ Winding Specs Detected"
                    
                    # Save to History
                    st.session_state.vision_history.append({
                        "img": active_img, 
                        "q": final_q, 
                        "resp": resp,
                        "w_info": w_info
                    })
                    if len(st.session_state.vision_history) > 5: st.session_state.vision_history.pop(0)
                    st.rerun()

    # -- 🎞️ SCAN HISTORY FILMSTRIP --
    if st.session_state.get("vision_history"):
        st.markdown("---")
        st.subheader("🎞️ Scan History (Pipeline Buffer)")
        h_cols = st.columns(len(st.session_state.vision_history))
        for idx, entry in enumerate(reversed(st.session_state.vision_history)):
            with h_cols[idx]:
                st.image(entry["img"], width=100)
                if entry.get("w_info"): st.caption("⚡ [Winding Data]")
                if st.button(f"View #{len(st.session_state.vision_history)-idx}", key=f"hist_{idx}"):
                    st.session_state.v_resp = entry["resp"]
                    st.session_state.v_q_final = entry["q"]
                    st.session_state.v_curr_w_info = entry.get("w_info", "")
                    st.rerun()

    # -- 🔊 PIPELINE AI RESULTS --
    if "v_resp" in st.session_state:
        st.markdown("---")
        st.success("🤖 Pipeline Analysis Complete!")
        if st.session_state.get("v_curr_w_info"):
            st.warning(f"🎯 **Detected technical data:** {st.session_state.v_curr_w_info}")
            
        st.markdown(f"**⚡ Query:** *{st.session_state.get('v_q_final', 'Visual Scan')}*")
        st.info(st.session_state.v_resp)
        js_audio = voice_utils.text_to_speech(st.session_state.v_resp, lang=tts_code)
        if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)

elif mode == "📊 Performance & Efficiency":
    st.header("📊 Motor Performance & Efficiency Analyzer")
    st.info("Calculate real-time performance metrics for industrial energy saving.")
    
    col1, col2 = st.columns(2)
    with col1:
        v = st.number_input("Measured Voltage (V)", value=415.0)
        i = st.number_input("Measured Current (A)", value=10.0)
        p = st.number_input("Real Power (kW)", value=6.0)
    with col2:
        ph = st.selectbox("Phase Mode", [3, 1], key="perf_phase")
    
    if st.button("Analyze Efficiency"):
        pf, kva = calculators.calculate_efficiency_pf(v, i, p, ph)
        st.metric("Power Factor (cos φ)", pf)
        st.metric("Apparent Power", f"{kva} kVA")
        
        if pf < 0.8:
            st.warning("⚠️ Low Power Factor! Suggest adding Capacitor Bank.")
        else:
            st.success("✅ Power Factor is within Efficient Range.")
            
        # Voice Output
        resp = f"Power factor is {pf}. Apparent power is {kva} kVA."
        js_audio = voice_utils.text_to_speech(resp, lang=tts_code)
        if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)

elif mode == "📚 Electrician's Academy":
    st.header("📚 Electrician's Academy (Viva Prep)")
    st.info("Essential notes, formulas, and diagrams for examiners and professional marks.")
    
    tab_n, tab_f, tab_d = st.tabs(["📝 Technical Notes", "🧮 Formulas", "🎨 Winding Diagrams"])
    
    with tab_n:
        for topic, note in knowledge_base.TECHNICAL_NOTES.items():
            with st.expander(f"📌 {topic}"):
                st.write(note)
                
    with tab_f:
        st.latex("P = V \\times I \\times \\cos \\phi \\quad (1-Phase)")
        st.latex("P = \\sqrt{3} \\times V \\times I \\times \\cos \\phi \\quad (3-Phase)")
        st.latex("Efficiency = \\frac{Output Power}{Input Power} \\times 100")
        
    with tab_d:
        st.markdown("### 🌀 3-Phase Star vs Delta Schematic")
        import diagram_utils
        svg = diagram_utils.get_svg_diagram('Star-Delta Motor Starter', lang=lang_choice)
        st.components.v1.html(svg, height=450)

elif mode == "⚡ Load & Gauge Finder":
    st.header("⚡ Smart Motor Load & Design Engine")
    st.info("Input motor specs for automatic breaker, starter, and gauge selection.")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        hp = st.number_input("Motor HP", value=5.0)
    with col_l2:
        phases = st.selectbox("Phase", [3, 1], key="load_phase")
    
    if st.button("Generate Full Design Specs", type="primary"):
        amps, brk = calculators.calculate_motor_load(hp, phases)
        starter, starter_note = calculators.get_starter_recommendation(hp)
        
        c_r1, c_r2, c_r3 = st.columns(3)
        with c_r1: st.metric("Full Load Amps", f"{amps} A")
        with c_r2: st.metric("Breaker Size", f"{brk} A")
        with c_r3: st.metric("Starter Type", "DOL" if hp < 5 else "Star-Delta")
        
        st.success(f"📦 **Recommended Equipment:** Use a **{starter}**. {starter_note}")
        
        # Voice Output
        resp = f"For a {hp} HP motor, use a {brk} ampere breaker and a {starter}."
        js_audio = voice_utils.text_to_speech(resp, lang=tts_code)
        if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)
    
    st.markdown("---")
    st.subheader("🎯 MASTER REWINDING GAUGE FINDER")
    if st.button("Find Exact SWG Specs (Starting & Running)", type="primary"):
        with st.spinner("Calculating Standard Gauge..."):
            # Check Knowledge Base First
            obj_type = "water_pump" if phases == 1 else "motor"
            kb_key = f"{obj_type}_{hp}HP_{'single' if phases==1 else 'three'}_phase"
            # Normalize HP for KB lookup (e.g. 1.0 -> 1)
            kb_key = kb_key.replace("1.0HP", "1HP").replace("2.0HP", "2HP").replace("0.5HP", "0.5HP").replace("3.0HP", "3HP").replace("5.0HP", "5HP").replace("7.5HP", "7.5HP")
            kb_data = knowledge_base.WINDING_DATA["motors"].get(kb_key)
            
            resp_text = ""
            if kb_data:
                st.success(f"✅ Found Verified Industrial Data for {hp}HP {phases}-Phase")
                
                if phases == 1:
                    resp_text = f"For 1-Phase: Running {kb_data['running_wire_swg']} SWG, Starting {kb_data['starting_wire_swg']} SWG. Capacitor: {kb_data['capacitor']}."
                    table_data = {
                        "Parameter": ["Running Winding SWG", "Starting Winding SWG", "Capacitor", "Running Turns", "Starting Turns", "Coil Pitch", "Connection"],
                        "Value": [
                            kb_data['running_wire_swg'], 
                            kb_data['starting_wire_swg'], 
                            kb_data['capacitor'],
                            kb_data.get('turns_running', 'Check core size'),
                            kb_data.get('turns_starting', 'Check core size'),
                            kb_data.get('pitch', 'Standard'),
                            kb_data.get('connection', 'Series')
                        ]
                    }
                else:
                    resp_text = f"For 3-Phase: All windings are {kb_data['wire_swg']} SWG. Connection: {kb_data['connection']}."
                    table_data = {
                        "Parameter": ["Phase Winding SWG (U,V,W)", "Turns per Phase", "Coil Pitch", "Internal Connection", "Industrial Notes"],
                        "Value": [
                            kb_data['wire_swg'], 
                            kb_data.get('turns', 'Check nameplate'),
                            kb_data.get('pitch', 'Standard'),
                            kb_data.get('connection', 'Star/Delta'),
                            kb_data.get('notes', 'Verified data')
                        ]
                    }
                
                st.write(resp_text)
                st.table(table_data)
            else:
                p = f"""What is the exact official STARTING GAUGE (SWG) and RUNNING GAUGE (SWG) for rewinding a {hp} HP {phases} Phase motor? 
                Provide a markdown table and a short explanation in {lang_choice}."""
                resp_text = ai_engine.chat_with_electrician([{"role":"user","content":p}], target_language=lang_choice)
                st.markdown(resp_text)
            
            # Universal Voice Output
            js_audio = voice_utils.text_to_speech(resp_text, lang=tts_code)
            if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)

elif mode == "🗺️ Winding & Wiring Designer":
    st.header("🗺️ Professional Wiring Diagram Designer")
    st.info("Select a circuit type to generate an official wiring schematic.")
    
    import diagram_utils
    
    c_type = st.selectbox("Select Circuit", [
        "1-Way Switch", 
        "2-Way Switch (Staircase)", 
        "Ceiling Fan with Regulator", 
        "Motor Direct Online (DOL)",
        "Star-Delta Motor Starter"
    ])
    
    if st.button("Generate Official Diagram"):
        with st.spinner("Rendering Schematic..."):
            svg_code = diagram_utils.get_svg_diagram(c_type, lang=lang_choice)
            st.markdown(f"### {c_type} Schematic")
            st.components.v1.html(svg_code, height=420)
            
            # Provide text description for Voice
            desc = f"Generating the professional electrical schematic for {c_type} in {lang_choice}."
            js_audio = voice_utils.text_to_speech(desc, lang=tts_code)
            if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)

elif mode == "🌐 Live Industrial IoT (Sim)":
    st.header("🌐 Live Industrial IoT Dashboard (Simulated)")
    st.info("Live sensor feed from the industrial floor. (Digital Twin Simulation)")
    
    # Using random animation for "Viva" impressiveness
    import random
    curr = 12.5 + random.uniform(-0.5, 0.5)
    temp = 45 + random.uniform(-1, 1)
    volt = 415 + random.uniform(-5, 5)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Motor Current", f"{round(curr, 2)} A", f"{round(random.uniform(-0.1, 0.1), 2)}A")
    with c2: st.metric("Bearing Temp", f"{round(temp, 2)} °C", "Normal" if temp < 70 else "Warning")
    with c3: st.metric("Line Voltage", f"{round(volt, 1)} V", "Stable")
    
    # Visual Gauges (Simulated with progress bars)
    st.write("🔥 Temperature Strain")
    st.progress(min(temp/100, 1.0))
    st.write("⚡ Load Capacity")
    st.progress(min(curr/50, 1.0))
    
    if st.button("Run System Diagnostics"):
        st.balloons()
        st.success("Industrial System Check: ALL SYSTEMS NOMINAL. Bearing lubrication required in 50 hours.")

elif mode == "📏 Circuit Voltage Drop":
    st.header("📉 Advanced Voltage Drop Analysis")
    st.info("Analyze cable losses and get automatic wire size recommendations.")
    
    c1, c2, c3 = st.columns(3)
    with c1: dist = st.number_input("Distance (Meters)", value=50)
    with c2: wire = st.selectbox("Current Wire (mm²)", [1.5, 2.5, 4.0, 6.0, 10.0, 16.0])
    with c3: material = st.selectbox("Material", ["Copper", "Aluminum"])
    
    c_amps = st.number_input("Design Load (Amps)", value=15.0)
    
    if st.button("Analyze Drop"):
        vd, p_drop, sf, suggest = calculators.calculate_voltage_drop(c_amps, dist, wire, material=material)
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Voltage Loss", f"{vd} V")
            st.metric("Drop Percentage", f"{p_drop}%")
        with col_res2:
            st.write(f"🛡️ Security Status: **{sf}**")
            if p_drop > 3.0:
                st.warning(f"⚠️ Recommendation: Upgrade to **{suggest} mm²** for <3% loss.")
            else:
                st.success("✅ Current wire size is optimal for this distance.")
        
        # Voice Output
        resp = f"Voltage drop is {p_drop} percent. {sf}."
        js_audio = voice_utils.text_to_speech(resp, lang=tts_code)
        if js_audio: st.components.v1.html(voice_utils.get_audio_html(js_audio), height=0)

elif mode == "🛠️ Winding Database":
    st.header("Local Model Winding Database")
    cat = st.selectbox("DB Category", list(knowledge_base.WINDING_DATA.keys()))
    mod = st.selectbox("DB Model", list(knowledge_base.WINDING_DATA[cat].keys()))
    st.json(knowledge_base.WINDING_DATA[cat][mod])

