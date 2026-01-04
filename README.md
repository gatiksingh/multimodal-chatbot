# 🧠 Multimodal Chatbot (Text + Image)

A multimodal AI chatbot that:
- Answers text queries using Qwen LLM
- Describes uploaded images using Qwen Vision
- Simple HTML/CSS frontend
- FastAPI backend

---

## 🚀 Features
- Text-based chat
- Image upload & description
- Hugging Face Inference API
- Clean UI with image preview

---

## 🛠 Tech Stack
- FastAPI
- HuggingFace Hub
- Qwen 2.5 Text & Vision Models
- HTML, CSS, JavaScript

## Working of Project
1. User Input
User sends a text message or image through API endpoints.
2. FastAPI Backend
FastAPI receives and validates the request.
Routes the request to:
 hf_text.py for text queries
 hf_vision.py for image queries(Default Promt is set to describe the image.)
3. Hugging Face API
Backend sends input to Hugging Face Inference API using a secure access token.
The AI model processes the input and generates a response.
4. Response Handling
Response is cleaned and structured.
JSON response is returned to the user.

User → FastAPI → Hugging Face Model → FastAPI → User

---

## ScreenShots
<img width="1919" height="976" alt="Screenshot 2026-01-04 104202" src="https://github.com/user-attachments/assets/baa90f49-b97f-4f87-b2d8-0bd38c740d0e" />
<img width="1919" height="963" alt="image" src="https://github.com/user-attachments/assets/b8e73c37-5c9d-4327-aaf8-d0c0ef1260ea" />
<img width="1919" height="917" alt="Screenshot 2026-01-04 104709" src="https://github.com/user-attachments/assets/876df1cb-510a-44cd-bdd5-a4e6955908ef" />
<img width="1919" height="905" alt="Screenshot 2026-01-04 104721" src="https://github.com/user-attachments/assets/f69d24a9-e7c3-4465-a6f4-e3b336a74b8a" />

---

## Difficulties While Implementaion of Project
Import & module linking issues while structuring FastAPI files
Environment variable loading errors (.env configuration)
Hugging Face API latency during first requests (cold start)
Windows permission errors while running Uvicorn
Understanding and designing a multimodal architecture

---

## 🔐 Security
API keys stored securely in .env
.env excluded using .gitignore
No hardcoded secrets in the codebase

---

📚 Learning Outcomes
Built an AI backend using FastAPI
Integrated LLMs and Vision models
Worked with real-world APIs and tokens
Understood multimodal AI workflows

---

🏁 Conclusion

This project demonstrates a scalable multimodal chatbot backend capable of handling both text and image inputs, suitable for hackathons, academic projects, and AI-based applications.

---

## ▶️ Run Locally

### Backend
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8081
