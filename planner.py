def decide_task_type(input_text):
    return (
        f"Analyze this input: \"{input_text}\"\n\n"
        f"Classify the topic type (e.g. 'basic', 'advanced', or 'project-based') "
        f"and decide what type of learning material is most appropriate to generate:\n"
        f"- If basic, return 'summary + quiz'\n"
        f"- If advanced, return 'lesson + quiz'\n"
        f"- If project-based, return 'lesson + project idea + quiz'\n"
        f"Only respond with the final decision string."
    )
