from groq import Groq
from bot.core.config import GROQ_API_KEY

async def get_ai_response(prompt: str) -> str:
    """Gets a response from the Groq AI model."""
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is not configured."

    try:
        client = Groq(api_key=GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error interacting with Groq API: {e}"
