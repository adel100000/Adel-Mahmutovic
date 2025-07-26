# StudyAI

StudyAI is an AI-powered educational assistant designed to enhance the studying experience. It features several intelligent tools including a YouTube summarizer, study plan generator, quiz generator, and a fully autonomous All-in-One agent that integrates all features into a single workflow.

The application is built using Streamlit and leverages the Google Gemini API to simulate a personalized tutor and study helper.

---

## Setup Instructions

1. **Clone the repository**

git clone https://github.com/adel100000/Adel-Mahmutovic
cd studyai



2. **Install required dependencies**

It's recommended to use a virtual environment:

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install streamlit google-generativeai python-dotenv firebase-admin requests uuid



You may add any other modules you used manually here as well.

3. **Environment Configuration**

Create a .env file in the root of the project with your Gemini API key:

GEMINI_API_KEY=your_gemini_key_here



Also ensure your Firebase key is placed in a .json file and is listed in .gitignore to prevent uploading it publicly.

---

## How to Run the Agent

1. Start the backend API by navigating to the correct path in your terminal and running:

python api.py



2. Start the frontend Streamlit interface by running:

python -m streamlit run app.py



The app will open in your browser. You can then use the following tools:

- YouTube Summarizer
- Study Plan Generator
- Quiz Generator
- All-in-One Agent (combines all tools into a single workflow)

---

## Dependencies

The main dependencies for this project include:

- streamlit
- google-generativeai
- python-dotenv
- firebase-admin
- requests
- uuid

Additional built-in modules used include: os, json, re, etc.

---

## Author

This project was built solo by Adel Mahmutovic for The ODSC-Google-Cloud Agentic AI Hackathon.

---

## Notes

- Be sure to keep the .json file and .env excluded from version control.
- For API usage limits or quota errors, refer to the Gemini API documentation.








































