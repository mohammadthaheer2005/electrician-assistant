import os
import io
import base64
from gtts import gTTS
import speech_recognition as sr

def text_to_speech(text: str, lang: str = 'en') -> str:
    """
    Converts text to speech using gTTS.
    Returns the base64 encoded audio string to be embedded in HTML/Streamlit.
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        # Save to memory instead of writing file
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
    md = f"""
        <audio autoplay class="stAudio">
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
        """
    return md

def process_audio_bytes(audio_bytes: bytes, lang_code: str = 'en-US') -> str:
    """
    Takes audio bytes from Streamlit audio recorder,
    converts it to text using SpeechRecognition.
    """
    try:
        r = sr.Recognizer()
        audio_data = sr.AudioData(audio_bytes, sample_rate=44100, sample_width=2)
        # Using Google Free Web Speech API with specific language hint
        text = r.recognize_google(audio_data, language=lang_code)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"Error processing audio: {e}"
