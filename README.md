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

---

## ▶️ Run Locally

### Backend
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8081
