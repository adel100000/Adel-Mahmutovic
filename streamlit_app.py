import streamlit as st
import requests

st.set_page_config(page_title="StudyAI 🔥", layout="centered")

st.title("📚 StudyAI: Your All-in-One Study Assistant")

# Define tabs
tab1, tab2, tab3 = st.tabs(["🧾 Summarize", "📅 Plan Generator", "❓ Quiz Generator"])

### --- Tab 1: Summarizer ---
with tab1:
    st.subheader("Summarize Any Topic")
    user_input = st.text_area("Enter a topic or paragraph:")
    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            res = requests.post("http://localhost:5000/summarize", json={"input": user_input})
            st.success(res.json().get("summary", "No summary returned."))

### --- Tab 2: Plan Generator ---
with tab2:
    st.subheader("Generate a Custom Study Plan")
    topic = st.text_input("Enter the topic for your study plan:")
    if st.button("Generate Plan"):
        with st.spinner("Planning..."):
            res = requests.post("http://localhost:5000/plan", json={"topic": topic})
            st.success(res.json().get("plan", "No plan returned."))

### --- Tab 3: Quiz Generator ---
with tab3:
    st.subheader("Generate Quiz Questions")
    quiz_topic = st.text_input("Enter topic to generate quiz questions:")
    num_questions = st.slider("Number of questions", 1, 10, 5)
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            res = requests.post("http://localhost:5000/quiz", json={
                "topic": quiz_topic,
                "count": num_questions
            })
            questions = res.json().get("questions", [])
            for i, q in enumerate(questions, start=1):
                st.markdown(f"**Q{i}:** {q}")
