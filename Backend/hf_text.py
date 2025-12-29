import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

# Load token
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize the client (Note: We use 'token' instead of 'api_key' for standard HF client)
client = InferenceClient(token=HF_TOKEN)

def generate_text_response(prompt: str) -> str:
    print("🤖 Qwen AI is thinking...")

    try:
        # We use Qwen2.5 because it is currently the most stable free model.
        # If you really want Qwen3, change this string to "Qwen/Qwen3-8B" (if available).
        model_id = "Qwen/Qwen2.5-72B-Instruct"

        completion = client.chat.completions.create(
            model=model_id, 
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500
        )

        # Extract the answer
        return completion.choices[0].message.content

    except Exception as e:
        print(f"❌ Error: {e}")
        return f"I couldn't connect to the AI model. Error: {e}"