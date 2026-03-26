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

def get_groq_client():
    import streamlit as st
    api_key = None
    try:
        # Check Streamlit Cloud Secrets first
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        # Fallback to local .env
        api_key = os.getenv("GROQ_API_KEY")
        
    if not api_key:
        return None
    return Groq(api_key=api_key)

def chat_with_electrician(messages: list, target_language: str = "en") -> str:
    """
    Sends conversational history to Groq Llama-3 model.
    """
    client = get_groq_client()
    if not client:
        return "Error: GROQ_API_KEY not found in Streamlit Secrets or .env file."
        
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

def analyze_image(image_base64: str, prompt: str) -> str:
    """
    Uses Hugging Face's serverless Vision API to analyze physical equipment.
    """
    import streamlit as st
    hf_key = None
    try:
        hf_key = st.secrets.get("HUGGING_FACE_API_KEY")
    except Exception:
        hf_key = HF_TOKEN
        
    if not hf_key:
        return "Error: HUGGING_FACE_API_KEY not found in Streamlit Secrets or .env file."
        
    try:
        hf_client = InferenceClient(api_key=hf_key)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are a master electrician. " + prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ]
        
        # Meta's Llama-3.2 11B Vision Instruct is free and highly capable on HF Serverless
        completion = hf_client.chat_completion(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct",
            messages=messages,
            max_tokens=800
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Vision Error: {str(e)}"
