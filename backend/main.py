from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai  # new client style
import re
import json

# Load .env
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body
class Idea(BaseModel):
    idea: str

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",  # valid Gemini 2.5 model
        contents=prompt
    )

    text = response.text.strip()

# Remove Markdown code block if present
    text = re.sub(r"^```json\s*|\s*```$", "", text, flags=re.DOTALL)

# Parse JSON
    try:
            result = json.loads(text)
    except Exception:
            result = {"error": "Could not parse JSON", "raw_text": text}

    return result
