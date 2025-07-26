import sys
import os
import streamlit as st
import requests

# App Config 
st.set_page_config(page_title="StudyAI Agent", page_icon="🎥", layout="centered")
st.title("🔍 StudyAI Agent")
st.markdown("Welcome! Get ready to learn — just pick a mode and go!")

# Agent Selector
mode = st.selectbox("🧠 Select Agent Mode", ["Video Summarizer", "Lesson Plan Generator", "Quiz Generator"])

# Summarizer Agent
if mode == "Video Summarizer":  # ✅ FIXED: removed space
    url = st.text_input("🎥 Paste YouTube URL:")
    if st.button("Summarize"):
        if not url.strip():
            st.warning("Please enter a valid YouTube URL.")
        else:
            with st.spinner("Fetching transcript and summarizing..."):
                try:
                    response = requests.post("http://localhost:5000/summarize", json={"url": url})
                    if response.status_code == 200:
                        summary = response.json().get("summary")
                        st.success("✅ Summary Ready!")
                        st.subheader("📝 AI Summary")
                        st.markdown(summary)
                        st.download_button("📥 Download Summary", data=summary, file_name="summary.md", mime="text/markdown")
                    else:
                        st.error("Error from backend.")
                except Exception as e:
                    st.error(f"Backend error: {e}")

# Lesson Plan Generator Agent
elif mode == "Lesson Plan Generator":
    topic = st.text_input("📚 Enter a Topic:")
    if st.button("Generate Lesson Plan"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating lesson plan..."):
                try:
                    response = requests.post("http://localhost:5000/plan", json={"topic": topic})
                    if response.status_code == 200:
                        plan = response.json().get("plan")
                        st.success("📋 Lesson Plan Ready!")
                        st.subheader("📚 AI-Generated Lesson Plan")
                        st.markdown(plan)
                        st.download_button("📥 Download Plan", data=plan, file_name="lesson_plan.md", mime="text/markdown")
                    else:
                        st.error("Error from backend.")
                except Exception as e:
                    st.error(f"Backend error: {e}")

# Quiz Generator Agent
elif mode == "Quiz Generator":
    topic = st.text_input("🧪 Topic for Quiz:")
    count = st.slider("🔢 Number of Questions", min_value=1, max_value=10, value=5)
    if st.button("Generate Quiz"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating quiz..."):
                try:
                    response = requests.post("http://localhost:5000/quiz", json={"topic": topic, "count": count})
                    if response.status_code == 200:
                        quiz_text = response.json().get("questions")
                        st.success("🧠 Quiz Ready!")
                        st.subheader("📝 AI-Generated Quiz")
                        st.markdown(quiz_text)
                        st.download_button("📥 Download Quiz", data=quiz_text, file_name="quiz.md", mime="text/markdown")
                    else:
                        st.error("Error from backend.")
                except Exception as e:
                    st.error(f"Backend error: {e}")

# Toolchain Agent Section
st.subheader("All-In-One-Agent")
user_toolchain_input = st.text_area("Enter content to analyze (e.g. transcript, article, notes)")
if st.button("🚀 Run Full Agent Chain"):
    if not user_toolchain_input.strip():
        st.warning("⚠️ Please enter some input first.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post("http://localhost:5000/api/toolchain", json={"text": user_toolchain_input})
                if response.status_code == 200:
                    results = response.json().get("results", {})
                    if results:
                        st.success("Agent Completed Autonomous Chain ✅")
                        full_output = ""

                        if "summary" in results:
                            st.subheader("📝 Summary")
                            st.markdown(results["summary"])
                            full_output += results["summary"] + "\n\n"

                        if "lesson_plan" in results:
                            st.subheader("📚 Lesson Plan")
                            st.markdown(results["lesson_plan"])
                            full_output += results["lesson_plan"] + "\n\n"

                        if "quiz" in results:
                            st.subheader("🧠 Quiz")
                            st.markdown(results["quiz"])
                            full_output += results["quiz"] + "\n\n"

                        st.download_button("📥 Download All Results", data=full_output, file_name="toolchain_output.md", mime="text/markdown")

                        # Gemini Next Step Suggestion
                        with st.spinner("🔮 Analyzing what to do next..."):
                            try:
                                next_step_response = requests.post("http://localhost:5000/next_step", json={"content": full_output})
                                if next_step_response.status_code == 200:
                                    suggestion = next_step_response.json().get("next_step", "")
                                    if suggestion:
                                        st.subheader("🧭 Suggested Next Step")
                                        st.markdown(suggestion)
                                else:
                                    st.warning("⚠️ Could not generate next step.")
                            except Exception as e:
                                st.warning(f"Next step error: {e}")
                    else:
                        st.error("❌ No output was returned.")
                else:
                    st.error("Backend error during toolchain execution.")
            except Exception as e:
                st.error(f"Backend error: {e}")

# My History Section
st.markdown("---")
st.subheader("📜 My Session History")

if st.button("🔄 Refresh History"):
    try:
        history_response = requests.get("http://localhost:5000/get_history")
        if history_response.status_code == 200:
            history_data = history_response.json()
            if not history_data:
                st.info("No history found yet.")
            else:
                for entry in history_data:
                    with st.expander(f"{entry.get('mode', 'Unknown Mode')} • {entry.get('timestamp', '')[:19].replace('T', ' ')}"):
                        st.markdown(f"**Input:**\n\n{entry.get('input', '')}")
                        output = entry.get('output', '')
                        if isinstance(output, dict):
                            for key, val in output.items():
                                st.markdown(f"**{key.title().replace('_', ' ')}:**\n\n{val}")
                        else:
                            st.markdown(f"**Output:**\n\n{output}")
        else:
            st.error("⚠️ Could not fetch history.")
    except Exception as e:
        st.error(f"Backend error: {e}")
