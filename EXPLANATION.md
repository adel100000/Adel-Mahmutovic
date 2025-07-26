Technical Explanation – StudyAI

1\. Agent Workflow

StudyAI follows a modular, tool-based agent workflow across four main study-assistance modes: Summarizer, Study Plan Generator, Quiz Generator, and the Autonomous Agent. Here’s a high-level breakdown of how the system processes input:



Receive user input via the selected mode in the Streamlit UI.



(Optional) Retrieve prior session memory from Firebase for continuity.



Plan sub-tasks (using logic from planner.py) depending on the selected mode:



For summarizer: fetch video transcript (if YouTube link), chunk, summarize.



For study plans: parse goal, extract timeframe, outline plan.



For quizzes: interpret subject + level, construct custom questions.



For autonomous agent: combine multiple subtasks dynamically.



Execute subtasks using backend modules and Gemini 1.5 Flash API.



Log interactions to Firebase (chat sessions, tool outputs).



Display output back to the user in the frontend (streamlit\_app.py).



2\. Key Modules

planner.py:

Interprets the user’s study goal or task and breaks it into actionable sub-steps (e.g., summarize → extract transcript → generate TL;DR). Especially important in the autonomous mode.



executor.py:

Runs specific sub-tasks using Gemini API or internal tools. Handles mode-specific logic such as API calls to YouTube, quiz formatting, and result structuring.



memory.py:

Interfaces with Firebase to store and retrieve user history. Also assists in session continuity for future expansion into persistent memory.



utils.py:

Houses shared utility functions such as text cleaning, quiz formatting helpers, and API request builders.



api.py:

Backend logic orchestrating API requests and calling necessary planner/executor functions per mode. It serves as the core behind-the-scenes routing logic for the frontend.



3\. Tool Integration

StudyAI integrates with several key tools and APIs:



Gemini 1.5 Flash API

Used for generating summaries, quizzes, and study plans with fast, lightweight output.



YouTube Transcript API

Pulls transcripts from YouTube URLs for the Summarizer module.



Firebase Realtime Database



Stores user sessions and logs for tracking.



Tracks chat history per mode.



Handles basic memory storage (through memory.py).



Google Cloud Functions (indirectly via Firebase)

Powers backend features like login, authentication, and logging logic.



4\. Observability \& Testing

Logging

All session logs and query outputs are stored in Firebase under user-specific nodes. This ensures session traceability and history review.



Testing

A basic execution flow can be tested by:



Running streamlit run streamlit\_app.py and selecting any mode.



Triggering inputs manually to verify Gemini integration.



Observing Firebase log updates.



Note: A full test path walkthrough is available in EXPLANATION.md.



5\. Known Limitations

No Natural Chat Interface

Users must manually select modes, as StudyAI is not designed to respond to open-ended chat inputs like a standard chatbot.



Quiz Format Issues

Quiz outputs, while functional, may occasionally have formatting inconsistencies—particularly in the autonomous mode.



Autonomous Mode Limitations

The autonomous agent cannot process YouTube video inputs directly. It is optimized for text input only.



Latency for Longer Prompts

Some delays may occur when processing long-form content or large YouTube transcripts.

