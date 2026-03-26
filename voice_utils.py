import os
import io
import base64
from gtts import gTTS
import speech_recognition as sr

def text_to_speech(text: str, lang: str = 'en') -> str:
    """
    Returns JS code to instantly speak the text using the browser's super natural neural OS voices (Alexa/Siri quality).
    """
    # Clean text of markdown asterisks and hash marks to avoid spelling them out
    clean_text = text.replace("*", "").replace("#", "").replace('"', "'").replace("\n", " ")
    
    js_code = f"""
    <script>
        const msg = new SpeechSynthesisUtterance("{clean_text}");
        msg.lang = "{lang}";
        
        // Try to find a premium local Google/Microsoft voice if available
        let voices = window.speechSynthesis.getVoices();
        let selectedVoice = voices.find(v => v.lang.includes("{lang}") && (v.name.includes("Google") || v.name.includes("Microsoft") || v.name.includes("Natural")));
        if (selectedVoice) {{
            msg.voice = selectedVoice;
        }}
        
        // Slight tweak for natural pacing
        msg.rate = 1.0; 
        msg.pitch = 1.0;
        
        window.speechSynthesis.speak(msg);
    </script>
    """
    return js_code

def get_audio_html(b64_audio: str) -> str:
    # b64_audio is now just the JS snippet
    return b64_audio

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
