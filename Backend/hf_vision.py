import os
import base64
import mimetypes
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"

def generate_vision_response(prompt: str, image_path: str) -> str:
    print("👁️ Qwen Vision is thinking...")

    try:
        # Detect MIME type (image/jpeg, image/png, etc.)
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = "image/jpeg"

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
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

        return completion.choices[0].message.content

    except Exception as e:
        print(f"❌ Vision Error: {e}")
        return f"Vision model error: {e}"
