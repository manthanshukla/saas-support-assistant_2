
import os
from openai import OpenAI
from dotenv import load_dotenv

from app.services.prompt import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_response(question, context, conversation=None):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if conversation:
        for msg in conversation[-10:]:
            if (
                isinstance(msg, dict)
                and msg.get("role") in ["user", "assistant"]
                and isinstance(msg.get("content"), str)
            ):
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

    messages.append({
        "role": "user",
        "content": f"""
Context:
{context}

Question:
{question}
"""
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content
