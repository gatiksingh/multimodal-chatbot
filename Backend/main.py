from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
import os
from pathlib import Path

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

# Create temp directory
TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)

@app.post("/chat")
async def chat(
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    try:
        # Case 1: IMAGE with optional TEXT
        if image:
            if not generate_vision_response:
                return {"reply": "Vision AI is not configured. Please contact support."}
            
            print(f"📸 Image detected: {image.filename}")
            
            # Save image temporarily with async read
            file_location = TEMP_DIR / f"temp_{image.filename}"
            with open(file_location, "wb") as f:
                content = await image.read()
                f.write(content)
            
            # Use custom prompt or auto-generate
            prompt = text.strip() if text and text.strip() else "Analyze this product image and provide a detailed description including features, design, materials, and potential use cases."
            
            response_text = generate_vision_response(prompt, str(file_location))
            
            # Cleanup
            try:
                os.remove(file_location)
            except Exception as e:
                print(f"⚠️ Cleanup warning: {e}")
            
            return {"reply": response_text}
        
        # Case 2: TEXT ONLY
        if text and text.strip():
            print(f"💬 Text detected: {text}")
            response_text = generate_text_response(text.strip())
            return {"reply": response_text}
        
        # Case 3: NOTHING PROVIDED
        return {"reply": "Please upload an image or type a message to get started!"}
    
    except Exception as e:
        print(f"❌ Error in /chat: {str(e)}")
        return {"reply": "Sorry, something went wrong. Please try again."}

@app.get("/")
async def root():
    return {
        "message": "AI Product Description Bot",
        "status": "online",
        "vision_enabled": generate_vision_response is not None
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}



