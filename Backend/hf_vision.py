import os
import base64
import mimetypes
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables!")

client = InferenceClient(api_key=HF_TOKEN)
MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"

VISION_SYSTEM_PROMPT = """You are a product image analysis assistant for an e-commerce platform.

Language & Tone:
- Respond ONLY in English
- Be professional, helpful, and descriptive
- Focus on factual observations

Product Image Analysis:
- Describe what you see clearly and accurately
- Focus on: product type, colors, materials, design features, condition
- Mention visible specifications, dimensions (if apparent), and notable details
- Suggest potential use cases or target audience when relevant
- If details are unclear, use phrases like "appears to be" or "seems to have"

Interaction Rules:
- Keep descriptions informative but concise (3-5 sentences)
- Ask ONE relevant follow-up question when appropriate
- Never criticize image quality or lighting
- Stay focused on helping customers understand the product

Remember: Describe what you see, not what you assume."""

def generate_vision_response(prompt: str, image_path: str) -> str:
    """Generate vision response using Qwen VL model"""
    print(f"👁️ Analyzing image: {image_path}")
    
    try:
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = "image/jpeg"
        
        # Read and encode image
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # Generate response
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
            max_tokens=400,
            temperature=0.7
        )
        
        response = completion.choices[0].message.content.strip()
        print("✅ Vision response generated")
        return response
        
    except FileNotFoundError:
        print(f"❌ Image file not found: {image_path}")
        return "I couldn't find the image file. Please try uploading again."
    
    except Exception as e:
        print(f"❌ Vision analysis error: {e}")
        return "I'm having trouble analyzing this image right now. Please try again with a different image or in a moment."
