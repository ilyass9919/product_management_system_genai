import os
import openai

openai.api_key = os.getenv("OPEN_AI_KEY")

def ask_ai(message, system_prompt="You are an AI Product Management assistant."):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        max_tokens=500
    )
    return response['choices'][0]['message']['content']
