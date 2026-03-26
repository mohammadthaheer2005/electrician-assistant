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

def process_audio_bytes(audio_bytes: bytes, groq_key: str = None, lang_code: str = 'en-US') -> str:
    """
    Takes audio bytes from Streamlit audio recorder,
    converts it to text using Groq's high-speed Whisper API for 100% reliability.
    """
    import os
    import streamlit as st
    from ai_engine import get_groq_client
    
    client = get_groq_client(groq_key)
    if not client:
        return "Error: GROQ_API_KEY is missing. Please paste it in the sidebar."

    try:
        # Groq expects a file-like object
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "speech.webm" # File extension helps the API identify format
        
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            prompt="Electrician terminology like volts, current, capacitor, hum, buzz, motor.", # Helps accuracy
            response_format="json",
            language=lang_code.split('-')[0] # Groq prefers 2-letter codes for audio
        )
        return transcription.text
            
    except Exception as e:
        return f"Voice Error (Groq): {str(e)}"
