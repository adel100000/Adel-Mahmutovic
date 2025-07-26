import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Missing Gemini API key. Make sure GEMINI_API_KEY is set in the .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Missing Gemini API key. Make sure GEMINI_API_KEY is set in the .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_text(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_summary(transcript):
    prompt = f"Summarize the following YouTube transcript in a concise way:\n\n{transcript}"
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_lesson(topic):
    prompt = f"Create a short and beginner-friendly lesson on the topic: {topic}. Explain it clearly for someone with no prior knowledge."
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_quiz(topic, count=5):
    prompt = f"Generate {count} quiz questions on the topic: {topic}"
    return generate_text(prompt)

