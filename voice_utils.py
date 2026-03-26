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
        # API URL for OpenAI Whisper Large V3 Turbo on HF Serverless
        API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
        headers = {"Authorization": f"Bearer {active_key}"}
        
        # Using a session for better connection persistence
        session = requests.Session()
        
        # Retry loop for 503 "Model is loading" or network hiccups
        max_retries = 3
        for i in range(max_retries):
            try:
                # Add a timeout to prevent hanging, and ensure data is sent fully
                response = session.post(API_URL, headers=headers, data=audio_bytes, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("text", "Sorry, no transcript was generated. Please try again.")
                elif response.status_code == 503 and i < max_retries - 1:
                    time.sleep(5)
                    continue
                else:
                    return f"Error: API status {response.status_code}. Response: {response.text[:200]}"
            except (requests.exceptions.ContentDecodingError, requests.exceptions.ConnectionError) as ce:
                if i < max_retries - 1:
                    time.sleep(2)
                    continue
                return f"Error: Persistent connection issue - {ce}"
            except Exception as e:
                return f"Error: {e}"
            
    except Exception as e:
        return f"Error processing audio with Whisper: {e}"
