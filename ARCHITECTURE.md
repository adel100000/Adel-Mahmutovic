\# Architecture Overview



This document outlines the high-level architecture of the StudyAI agent system, including its planner, executor, memory, tool integrations, and observability components.







## System Diagram (ASCII Sketch)



                  +----------------------+

                  |     User Interface   |

                  |   (Streamlit Frontend)|

                  +----------+-----------+

                             |

                             v
                  +----------+-----------+

                  |     Flask Backend     |

                  |  (API Gateway Layer)  |

                +----------+-----------+

                           |

      +---------------------+---------------------+

       |                     |                     |

       v                     v                     v

+---------------+   +-----------------+   +----------------------+

|    Planner    |   |    Executor     |   |     Memory Module    |

| (planner.py)  |   | (executor.py)   |   | (memory.py + Firebase)|

+---------------+   +-----------------+   +----------------------+

                       |      |

                       |      v

                       |   Gemini API

                       | (Text/Quiz/Lesson)

                       v

              +----------------------+

              | Toolchain Logic Flow |

              |    + utils.py        |

              +----------------------+







\## Components



\### 1. \*\*User Interface (Frontend)\*\*

\- \*\*Streamlit UI\*\* (app.py)

 - User selects one of three modes: Summarizer, Quiz Generator, Lesson Planner.

 - Also includes an autonomous "Toolchain" runner.

 - Handles data input (YouTube links, topics) and output rendering.

 - Communicates with Flask backend via REST API (requests.post() calls).



---



\### 2. \*\*Agent Core (Backend)\*\*



\#### Planner — planner.py

\- Decides how to route user input by prompting Gemini to classify it.

\- Determines the correct tools to call: summary, lesson, quiz, or all three.



\#### Executor — executor.py

\- Interfaces with Gemini API to generate:

 - Summaries of video transcripts

 - Full lesson plans

 - Custom quizzes

\- Handles prompting, result formatting, and model-specific logic.



\#### Toolchain Logic — api.py

\- Flask backend handles all API endpoints for:

 - /plan, /quiz, /summarize, /api/toolchain, /next\_step, etc.

\- Orchestrates planner → executor → memory chain based on request mode.



---



\### 3. \*\*Memory (Persistent + Session)\*\*



\#### Firebase (Firestore + Realtime DB)

\- Used to persist:

 - Summaries, quizzes, and plans (db.reference().push(...))

 - Session history (fs.collection("history").stream())

\- Enables session recall and browsing through the frontend.



\#### Local Cache (optional)

\- Python-side memory.py handles bridging between backend and Firebase.

\- No local file cache used for now, but extendable.



---



\### 4. \*\*Tools \& APIs\*\*



\#### Gemini API (via executor.py)

\- All text-based tasks (summarization, lesson planning, quizzes) are handled through the Gemini LLM.

\- Toolchain logic dynamically builds prompts and delegates to Gemini.



\#### YouTube Transcript API

\- Utilized by utils.py to fetch transcripts from public YouTube videos.

\- Supports summarizer mode.



---



\### 5. \*\*Observability \& Logging\*\*



\#### Logging

\- Simple logging and observability through:

 - print() debugging in Streamlit and Flask

 - Firebase logs of user inputs and generated outputs



\#### Error Handling

\- Frontend and backend both return structured errors (status code 400+)

\- Gracefully handles:

 - Invalid YouTube URLs

 - Gemini API failures

 - Firebase connection issues



---



\## Additional Notes



\-Frontend and backend are both separate folders within the src file

 - This is acceptable as long as they’re linked correctly as \src and documented in `README.md`.

\- .env file securely loads Firebase credentials.

\- .gitignore excludes the credential file and any local logs.

















