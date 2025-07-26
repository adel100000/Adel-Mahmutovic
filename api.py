from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db, firestore
from planner import decide_task_type
from executor import (
    generate_text, generate_summary, generate_lesson,
    generate_quiz
)
from memory import save_to_history
from utils import get_youtube_transcript
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase safely
if not firebase_admin._apps:
    firebase_path = os.getenv("FIREBASE_CRED_PATH")
    if not firebase_path:
        raise ValueError("FIREBASE_CRED_PATH environment variable not set.")
    
    cred = credentials.Certificate(firebase_path)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://studyai-5ea51-default-rtdb.firebaseio.com"
    })

# Firestore DB (for history)
fs = firestore.client()

# Flask setup
app = Flask(__name__)
CORS(app)

@app.route("/plan", methods=["POST"])
def plan():
    topic = request.get_json().get("topic", "")
    result = generate_lesson(topic)
    db.reference("/plans").push({"topic": topic, "plan": result})
    save_to_history({"mode": "Lesson Plan", "input": topic, "output": result})
    return jsonify({"plan": result})

@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json()
    topic = data.get("topic", "")
    count = int(data.get("count", 5))
    result = generate_quiz(topic, count)
    db.reference("/quizzes").push({"topic": topic, "count": count, "questions": result})
    save_to_history({"mode": "Quiz", "input": topic, "output": result})
    return jsonify({"questions": result})

@app.route("/summarize", methods=["POST"])
def summarize():
    url = request.get_json().get("url", "")
    transcript = get_youtube_transcript(url)
    if transcript.startswith("Error"):
        return jsonify({"summary": transcript}), 400
    summary = generate_text(f"Summarize this educational video transcript:\n\n{transcript}")
    db.reference("/summaries").push({"url": url, "summary": summary})
    save_to_history({"mode": "Summarizer", "input": url, "output": summary})
    return jsonify({"summary": summary})

@app.route("/api/toolchain", methods=["POST"])
def run_toolchain():
    input_text = request.get_json().get("text", "")
    decision_prompt = decide_task_type(input_text)
    decision = generate_text(decision_prompt).lower()
    results = {}

    if "summary" in decision:
        results["summary"] = generate_summary(input_text)
    if "lesson" in decision:
        results["lesson_plan"] = generate_lesson(input_text)
    if "quiz" in decision:
        results["quiz"] = generate_quiz(input_text)

    db.reference("/toolchain").push({"input": input_text, "decision": decision, "results": results})
    save_to_history({"mode": "Autonomous Toolchain", "input": input_text, "output": results})
    return jsonify({"decision": decision, "results": results})

@app.route("/next_step", methods=["POST"])
def next_step():
    content = request.get_json().get("content", "")
    prompt = f"Given this educational content:\n\n{content}\n\nSuggest the next step for the learner."
    suggestion = generate_text(prompt)
    return jsonify({"next_step": suggestion})

@app.route("/get_history", methods=["GET"])
def get_history():
    docs = fs.collection("history").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()
    return jsonify([{**doc.to_dict(), "id": doc.id} for doc in docs])

if __name__ == "__main__":
    app.run(debug=True)
