from fastapi import FastAPI, Form, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
import uvicorn
from typing import Optional
import os
from pathlib import Path
import shutil

# Import your existing logic
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

TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)

# Helper function to delete file (used by BackgroundTasks)
def cleanup_file(path: Path):
    if path.exists():
        try:
            os.remove(path)
            print(f"🧹 Cleaned up: {path}")
        except Exception as e:
            print(f"⚠️ Error cleaning up {path}: {e}")

@app.post("/chat")
async def chat(
    background_tasks: BackgroundTasks,  # <--- Added this
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    try:
        # --- Case 1: IMAGE with Optional Text ---
        if image:
            if not generate_vision_response:
                return {"reply": "Vision AI is not configured."}
            
            print(f"📸 Image detected: {image.filename}")
            
            # Save file safely
            file_location = TEMP_DIR / f"temp_{os.urandom(4).hex()}_{image.filename}"
            with open(file_location, "wb") as f:
                content = await image.read()
                f.write(content)
            
            # Schedule cleanup to happen AFTER response is sent
            background_tasks.add_task(cleanup_file, file_location)

            # Determine Prompt
            prompt = text.strip() if text and text.strip() else "Describe this product image in detail."

            # RUN BLOCKING CODE IN THREADPOOL (Non-blocking)
            response_text = await run_in_threadpool(generate_vision_response, prompt, str(file_location))
            
            return {"reply": response_text}
        
        # --- Case 2: TEXT ONLY ---
        if text and text.strip():
            print(f"💬 Text detected: {text}")
            
            # RUN BLOCKING CODE IN THREADPOOL
            response_text = await run_in_threadpool(generate_text_response, text.strip())
            
            return {"reply": response_text}
        
        # --- Case 3: EMPTY ---
        return {"reply": "Please upload an image or type a message!"}
    
    except Exception as e:
        print(f"❌ Error in /chat: {str(e)}")
        return {"reply": "Sorry, something went wrong. Please try again."}

@app.get("/")
async def root():
    return {"status": "online", "model": "Qwen 2.5"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
