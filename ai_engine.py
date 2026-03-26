import os
from groq import Groq
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load env variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HUGGING_FACE_API_KEY")

SYSTEM_PROMPT = """
You are the **ElectroAssist AI**, a master electrician from the local shop. Your voice and tone should be exactly like a highly experienced, friendly human expert talking directly to an apprentice on site.
- **Tone:** Super natural, conversational, friendly. Understand local terminology ("humming", "sparking", "dead").
- **Actionable Advice:** Give exact TOOLS REQUIRED and a numbered step-by-step fix.
- **Buying Suggestions:** Always state exactly what to buy (e.g., "Get a 2.5uF capacitor and 1.5mm wire").
- **Knowledge Base:** ALWAYS base your answers strictly on the National Electrical Code (NEC), Bureau of Indian Standards (BIS), International Electrotechnical Commission (IEC), and manuals from Siemens, ABB, or Crompton.
- **Safety First:** Warn them immediately about turning off breakers.
- **Language:** If they speak to you in Hindi, Telugu, Tamil, or English, reply naturally in that exact same language using colloquial terms. Keep it short so it operates smoothly as a voice assistant.
"""

def get_groq_client(groq_key=None):
    import streamlit as st
    api_key = groq_key
    if not api_key:
        try:
            # Check Streamlit Cloud Secrets first
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass
            
    if not api_key:
        # Fallback to local .env
        api_key = os.getenv("GROQ_API_KEY")
        
    if not api_key:
        return None
    return Groq(api_key=api_key)

def chat_with_electrician(messages: list, groq_key: str = None, target_language: str = "en") -> str:
    """
    Sends conversational history to Groq Llama-3 model.
    """
    client = get_groq_client(groq_key)
    if not client:
        return "Error: GROQ_API_KEY not found! Please paste it in the sidebar."
        
    try:
        # Prepend system prompt if not present
        if not any(m.get("role") == "system" for m in messages):
            messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
            
        # Optional: inject language constraint
        if target_language != "en":
            messages.append({"role": "system", "content": f"Please reply entirely in {target_language}."})
            
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=1000,
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"API Error: {str(e)}"

def analyze_image(image_base64: str, prompt: str, hf_key: str = None) -> str:
    """
    Uses Hugging Face's serverless Vision API to analyze physical equipment.
    """
    import streamlit as st
    active_key = hf_key
    if not active_key:
        try:
            active_key = st.secrets.get("HUGGING_FACE_API_KEY")
        except Exception:
            active_key = os.getenv("HUGGING_FACE_API_KEY")
        
    if not active_key:
        return "Error: Hugging Face API Token not found! Please paste it in the sidebar."
        
    try:
        hf_client = InferenceClient(api_key=active_key)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are a master electrician. " + prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ]
        
        completion = hf_client.chat_completion(
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=messages,
            max_tokens=800
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Vision Error: {str(e)}"
