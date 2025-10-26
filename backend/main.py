from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai
import re
import json

# Load .env
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body
class Idea(BaseModel):
    idea: str


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/generate")
def generate_pitch(data: Idea):
    prompt = f"""
    You are a startup pitch creator. Turn this idea into:
    1. Company Name
    2. Tagline
    3. Problem
    4. Solution
    5. Elevator Pitch

    Respond ONLY in JSON format.
    Idea: {data.idea}
    """

    # ✅ Correct Gemini API usage
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    text = response.text.strip()

    # ✅ Clean JSON if Gemini wrapped it in code block
    text = re.sub(r"^```json\s*|\s*```$", "", text, flags=re.DOTALL)

    try:
        result = json.loads(text)
    except Exception:
        result = {"error": "Could not parse JSON", "raw_text": text}

    return result
