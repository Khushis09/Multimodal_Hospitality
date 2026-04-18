# Multimodal Hospitality Creator

An AI-powered web application that generates **luxury hospitality descriptions + images** from user prompts.

## Features

*  AI-generated hotel/resort descriptions
*  Image generation using HuggingFace
*  Voice input support
*  Fast & interactive UI using Streamlit
*  Responsive modern UI
*  Session-based history storage

---

##  Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **LLM:** OpenRouter (Mistral / Mixtral)
* **Image Generation:** HuggingFace (Stable Diffusion)
* **Language:** Python

---

##  Setup Instructions

### 1. Clone repo

```bash
git clone https://github.com/Khushis09/Multimodal_Hospitality
cd Multimodal_Hospitality
```

### 2. Setup backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Setup frontend

```bash
cd ../frontend_streamlit
pip install -r requirements.txt
streamlit run app.py
```

---

## Environment Variables

Create `.env` inside backend:

```
OPENROUTER_API_KEY=your_key
HUGGINGFACE_API_KEY=your_key
```

---

## Demo

👉 Generates luxury hotel descriptions + images from prompts like:

* "hotel near beach"
* "resort near mountains"

---

## Future Improvements

* Chatbot assistant
* Persistent database (MongoDB / Firebase)
* Deployment (Streamlit Cloud / Render)
* Better image models

---

## Author

Khushi Singh
