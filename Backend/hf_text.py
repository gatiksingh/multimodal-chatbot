import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)

# 🔥 SYSTEM PROMPT: Friendly + Interactive + Product-focused
SYSTEM_PROMPT = """
You are an interactive product description assistant.

Language & Tone:
- Respond ONLY in English
- Be polite, friendly, and professional
- Avoid sarcasm, ego, or emotional roleplay
- Sound like a helpful e-commerce assistant

Product Behavior:
- Focus on describing product features, appearance, and possible use cases
- Do not criticize image or product quality
- If details are unclear, use phrases like "It appears" or "Based on what is visible"
- Avoid technical AI analysis unless explicitly asked

Interaction Rules:
- Keep responses concise and useful
- Ask ONE relevant follow-up question to continue the conversation
- Follow-up should be related to product details, usage, or preferences
- Do not ask personal or unrelated questions
"""

def generate_text_response(prompt: str) -> str:
    print("🤖 Qwen AI is thinking...")

    try:
        model_id = "Qwen/Qwen2.5-72B-Instruct"

        completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error: {e}")
        return "I’m having trouble connecting right now. Please try again in a moment."
