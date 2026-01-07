import os
import base64
import mimetypes
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"

# 🔥 SYSTEM PROMPT FOR PRODUCT IMAGE DESCRIPTION
VISION_SYSTEM_PROMPT = """
You are an interactive product image description assistant.

Language & Tone:
- Respond ONLY in English
- Be polite, professional, and customer-friendly
- Do not use slang, sarcasm, or emotional roleplay

Product Description Rules:
- Describe visible product features clearly
- Focus on design, appearance, and possible use cases
- Never criticize image quality, lighting, or clarity
- If details are unclear, say "It appears" or "Based on the image"

Interaction Rules:
- Keep responses concise and informative
- Ask ONE relevant follow-up question to continue the conversation
- Follow-up should relate to product details, usage, or preferences
- Do not ask personal or unrelated questions

You are not a chatbot friend.
You are an e-commerce product assistant.
"""

def generate_vision_response(prompt: str, image_path: str) -> str:
    print("👁️ Qwen Vision is thinking...")

    try:
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = "image/jpeg"

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": VISION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Vision Error: {e}")
        return "I’m having trouble analyzing the image right now. Please try again."

