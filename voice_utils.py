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

def listen_local_mic(lang_code: str = 'en-IN') -> str:
    """
    Uses local system microphone (requires PyAudio) for lightning-fast voice input.
    Best for local testing or 'Command Center' style apps on personal laptops.
    """
    try:
        import speech_recognition as sr
        # PyAudio check
        import pyaudio
    except ImportError:
        return "Error: PyAudio not installed. Run 'pip install pyaudio' on your local computer to use this feature."
    
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            # Short timeout for 'Command Center' feel
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            text = r.recognize_google(audio, language=lang_code)
            return text
    except sr.UnknownValueError:
        return "Error: Could not understand audio."
    except sr.RequestError as e:
        return f"Error: Google Speech service failed; {e}"
    except Exception as e:
        return f"Error: {e}"

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
        import requests
        
        # Whisper v3 Turbo endpoint
        API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
        headers = {"Authorization": f"Bearer {active_key}", "Content-Type": "audio/webm"}
        
        max_retries = 3
        for i in range(max_retries):
            try:
                # Use standard requests for better control and reliability
                response = requests.post(API_URL, headers=headers, data=audio_bytes, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, dict) and "text" in result:
                        return result["text"]
                    return str(result)
                elif response.status_code == 503:
                    # Model is loading
                    time.sleep(5)
                    continue
                else:
                    return f"Error: HF API {response.status_code} - {response.text}"

            except Exception as e:
                if i < max_retries - 1:
                    time.sleep(2)
                    continue
                return f"Error: {e}"
            
    except Exception as e:
        return f"Error processing audio with Whisper: {e}"
