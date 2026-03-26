import os
import io
import base64
from gtts import gTTS
import speech_recognition as sr

def text_to_speech(text: str, lang: str = 'en') -> str:
    """
    Converts text to speech using gTTS for guaranteed multilingual support on all browsers.
    """
    from gtts import gTTS
    import io
    import base64
    try:
        # gTTS uses 2-letter codes most of the time (en, te, hi, ml, ta)
        g_lang = lang.split('-')[0]
        
        # Clean text of markdown
        clean_text = text.replace("*", "").replace("#", "")
        
        tts = gTTS(text=clean_text, lang=g_lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Base64 encode
        audio_bytes = fp.read()
        b64 = base64.b64encode(audio_bytes).decode()
        return b64
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

def get_audio_html(b64_audio: str) -> str:
    """Returns HTML for auto-playing audio."""
    if not b64_audio:
        return ""
    md = f"""
        <audio autoplay class="stAudio">
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
        """
    return md

def process_audio_bytes(audio_bytes: bytes, hf_key: str = None, lang_code: str = 'en-US') -> str:
    """
    Takes audio bytes from Streamlit audio recorder,
    converts it to text using Hugging Face Whisper API for true Alexa-like robustness.
    """
    import os
    import requests
    import streamlit as st
    
    active_key = hf_key
    if not active_key:
        try:
            active_key = st.secrets.get("HUGGING_FACE_API_KEY")
        except Exception:
            pass
            
    if not active_key:
        from dotenv import load_dotenv
        load_dotenv()
        active_key = os.getenv("HUGGING_FACE_API_KEY")

    if not active_key:
        return "Error: Hugging Face API key is missing. Please paste it in the sidebar to enable Whisper STT."

    try:
        import time
        from huggingface_hub import InferenceClient
        
        # Retry loop for 503 "Model is loading" or network hiccups
        max_retries = 3
        for i in range(max_retries):
            try:
                # Use the official InferenceClient post method for full control over headers
                hf_client = InferenceClient(api_key=active_key)
                
                # audio-recorder-streamlit sends webm or wav depending on browser
                # audio/webm is widely supported by Whisper on HF
                response_data = hf_client.post(
                    data=audio_bytes,
                    model="openai/whisper-large-v3-turbo",
                    headers={"Content-Type": "audio/webm"}
                )
                
                import json
                result = json.loads(response_data.decode())
                
                if isinstance(result, dict) and "text" in result:
                    return result["text"]
                elif isinstance(result, str):
                    return result
                else:
                    return f"Error: Unexpected response format {result}"

            except Exception as e:
                # Catch 503 and retry
                if "503" in str(e) and i < max_retries - 1:
                    time.sleep(5)
                    continue
                # Catch Connection errors and retry once
                if "Connection" in str(e) and i < max_retries - 1:
                    time.sleep(2)
                    continue
                return f"Error: {e}"
            
    except Exception as e:
        return f"Error processing audio with Whisper: {e}"
