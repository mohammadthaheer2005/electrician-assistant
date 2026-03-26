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

def process_audio_bytes(audio_bytes: bytes, lang_code: str = 'en-US') -> str:
    """
    Takes audio bytes from Streamlit audio recorder,
    converts it to text using Hugging Face Whisper API for true Alexa-like robustness.
    """
    import os
    import requests
    import streamlit as st
    
    hf_key = None
    try:
        hf_key = st.secrets.get("HUGGING_FACE_API_KEY")
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()
        hf_key = os.getenv("HUGGING_FACE_API_KEY")

    if not hf_key:
        return "Error: Hugging Face API key is missing. Please add it to your secrets to enable Whisper STT."

    try:
        # API URL for OpenAI Whisper Large V3 Turbo on HF Serverless
        API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
        headers = {"Authorization": f"Bearer {hf_key}"}
        
        # Whisper automatically detects the language, but sending data directly works best
        response = requests.post(API_URL, headers=headers, data=audio_bytes)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("text", "Sorry, no transcript was generated. Please try again.")
        else:
            return f"Error: API returned status {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error processing audio with Whisper: {e}"
