import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables!")

client = InferenceClient(token=HF_TOKEN)

SYSTEM_PROMPT = """You are a helpful product description assistant for an e-commerce platform.

Language & Tone:
- Respond ONLY in English
- Be friendly, professional, and concise
- Avoid unnecessary jargon or overly technical language

Product Behavior:
- Focus on describing products, features, specifications, and use cases
- Provide practical information that helps customers make informed decisions
- If uncertain about details, acknowledge it honestly

Interaction Rules:
- Keep responses clear and to-the-point (2-4 sentences ideal)
- Ask ONE relevant follow-up question when appropriate
- Stay focused on product-related topics
- Be helpful without being pushy

Remember: You're an assistant, not a salesperson."""

def generate_text_response(prompt: str) -> str:
    """Generate text response using Qwen model"""
    print("🤖 Generating text response...")
    
    try:
        model_id = "Qwen/Qwen2.5-72B-Instruct"
        
        completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        response = completion.choices[0].message.content.strip()
        print("✅ Text response generated")
        return response
        
    except Exception as e:
        print(f"❌ Text generation error: {e}")
        return "I'm having trouble processing your request right now. Please try again in a moment."


