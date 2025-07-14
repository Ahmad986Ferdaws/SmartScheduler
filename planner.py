# app/planner.py

import openai
import os

openai.api_key = os.getenv(\"OPENAI_API_KEY\")

def generate_schedule(prompt=\"Block 2 hours for deep work every afternoon and add a daily standup at 9 AM.\"):
    system_prompt = (
        \"You are an AI assistant that creates a structured weekly schedule plan "
        "in JSON. For each event, return: title, day, start_time, duration_mins, and optional notes.\"
    )
    response = openai.ChatCompletion.create(
        model=\"gpt-4o\",
        messages=[
            {\"role\": \"system\", \"content\": system_prompt},
            {\"role\": \"user\", \"content\": prompt}
        ]
    )

    text = response.choices[0].message.content
    try:
        # The model returns a JSON block. Extract it.
        import json
        events = json.loads(text)
    except Exception:
        events = []
    return events

if __name__ == \"__main__\":
    result = generate_schedule()
    print(\"Generated Events:\", result)
