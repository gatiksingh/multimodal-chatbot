from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional

from hf_text import generate_text_response

try:
    from hf_vision import generate_vision_response
except ImportError:
    generate_vision_response = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):

    # IMAGE → Vision Model
    if image:
        if not generate_vision_response:
            return {"reply": "Vision AI is not configured."}

        print(f"📸 Image detected: {image.filename}")

        file_location = f"temp_{image.filename}"
        with open(file_location, "wb") as f:
            f.write(image.file.read())

        # 🔥 AUTO PROMPT if text missing
        prompt = text.strip() if text and text.strip() else "Describe this image in detail."

        response_text = generate_vision_response(prompt, file_location)
        return {"reply": response_text}

    # TEXT ONLY → LLM
    if text:
        print(f"💬 Text detected: {text}")
        response_text = generate_text_response(text)
        return {"reply": response_text}

    return {"reply": "Please provide text or an image."}


