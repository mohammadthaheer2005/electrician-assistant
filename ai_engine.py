import os
from groq import Groq
from dotenv import load_dotenv

# Load env variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """
You are the **ElectroAssist AI**, a highly skilled, certified master electrician.
Your job is to assist electricians with accurate, code-compliant answers regarding:
1. Motor Winding (Starting/Running coils)
2. Wire Gauge calculation (mm2 / SWG)
3. Voltage drops and Load Amperage.

Rules:
- ALWAYS prioritize electrical safety (e.g., recommend breakers, ground fault protection).
- If the user asks for wire sizes or gauge, reference standard Copper SWG/AWG/mm2 ampacity charts.
- Keep answers professional, concise, and easy to read on a mobile device while working on-site.
- If asked in a specific language (Hindi, Tamil, Spanish, etc.), reply in that SAME language.
- DO NOT hallucinate winding data; if you are unsure, provide standard formulas and advise them to check the motor nameplate.
"""

def get_groq_client():
    if not GROQ_API_KEY:
        return None
    return Groq(api_key=GROQ_API_KEY)

def chat_with_electrician(messages: list, target_language: str = "en") -> str:
    """
    Sends conversational history to Groq Llama-3 model.
    """
    client = get_groq_client()
    if not client:
        return "Error: GROQ_API_KEY not found in .env file."
        
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
    Uses Groq's Vision model to analyze electrical components.
    """
    client = get_groq_client()
    if not client:
        return "Error: GROQ_API_KEY not found."
        
    try:
        messages = [
            {"role": "system", "content": "You are a master electrician diagnosing visual issues from photos."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ]
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=messages,
            temperature=0.2,
            max_tokens=800
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Vision Error: {str(e)}"
