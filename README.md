# FastAPI + OpenAI Sample Integration

This project provides a simple FastAPI service integrated with OpenAI. It exposes two endpoints:

- `POST /generate-text` — A coding assistant that responds like a pirate.  
- `POST /generate-image` — Generates images in anime style.

## 🧪 Local Deployment

1. Set your OpenAI key:

```bash
export OPEN_API_KEY=your-api-key
```
Create and activate a virtual environment:

```bash
python3 -m venv openai
source openai/bin/activate
```
Install dependencies and run the server:
```bash
pip install -r requirements.txt
python3 main.py
```
The API will be available at a randomly assigned port, shown in the terminal.
🐳 Container Deployment
```bash
docker build -t openai .
docker run -p 9000:8080 openai
```
☁️ Cloud Deployment (Google Cloud Run)
```bash
gcloud run deploy SERVICE_NAME --region=YOUR_REGION --source . --allow-unauthenticated
```

## Resources used 
http://github.com/openai/openai-python
https://platform.openai.com/docs/libraries
https://www.youtube.com/watch?v=sXah_wSquFg&t=1462s

ChatGPT was used for README.md formatting

Used a sample code from a personal project for the find free port function.