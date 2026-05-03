import os
import asyncio
from google import genai
from bot.core.config import GEMINI_API_KEY

# Initialize the Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_FILE = os.path.join(BASE_DIR, "knowledge_base.txt")

# ✅ Helper to run blocking Gemini calls without freezing the bot
def _generate(model, system_instruction, contents):
    response = client.models.generate_content(
        model=model,
        config={"system_instruction": system_instruction},
        contents=contents,
    )
    return response.text

async def get_summary(text: str) -> str:
    try:
        return await asyncio.to_thread(
            _generate,
            "gemini-2.5-flash",
            "You are an expert engineer. Summarize this text into clear bullet points.",
            text
        )
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

async def generate_prompt(raw_idea: str) -> str:
    try:
        return await asyncio.to_thread(
            _generate,
            "gemini-2.5-flash",
            "You are an expert Prompt Engineer. Use the RTF framework to generate a detailed, structured prompt.",
            raw_idea
        )
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

async def suggest_commit(description: str) -> str:
    try:
        return await asyncio.to_thread(
            _generate,
            "gemini-2.5-flash",
            "Convert this to a professional Conventional Commit message with a short title and bullet points.",
            description
        )
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

async def analyze_error(log: str) -> str:
    try:
        return await asyncio.to_thread(
            _generate,
            "gemini-2.5-flash",
            "Analyze this error log and suggest 3 clear fix steps.",
            log
        )
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

async def quick_explain(concept: str) -> str:
    try:
        return await asyncio.to_thread(
            _generate,
            "gemini-2.5-flash",  # ← Change from gemini-2.0-flash
            "You are a patient teacher. Explain this concept or code simply and clearly in 3-4 sentences with a practical example.",
            concept
        )
    except Exception as e:
        return f"❌ Error: {str(e)}"

def save_to_kb(text: str):
    try:
        with open(KB_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n--- Entry ---\n{text}\n")
        print(f"DEBUG: Successfully wrote to {KB_FILE}")
    except Exception as e:
        print(f"DEBUG: Failed to write file: {e}")

async def search_kb(query: str) -> str:
    if not os.path.exists(KB_FILE) or os.path.getsize(KB_FILE) == 0:
        return "Your knowledge base is currently empty. Use /save first!"

    with open(KB_FILE, "r", encoding="utf-8") as f:
        context = f.read()

    try:
        system_instruction = (
            "You are a Knowledge Assistant. Use the provided 'Context' (which is the user's saved notes) "
            "to answer the user's query. If the answer isn't in the notes, say you don't know."
        )
        return await asyncio.to_thread(
            _generate,
            "gemini-2.5-flash",
            system_instruction,
            f"Context: {context}\n\nQuestion: {query}"
        )
    except Exception as e:
        return f"❌ Search Error: {str(e)}"

def clear_kb_file():
    try:
        with open(KB_FILE, "w", encoding="utf-8") as f:
            f.write("")
        print(f"DEBUG: Knowledge base at {KB_FILE} cleared.")
        return True
    except Exception as e:
        print(f"DEBUG: Failed to clear KB: {e}")
        return False


async def get_daily_tip() -> str:
    try:
        return await asyncio.to_thread(
            _generate,
            "gemini-2.5-flash",
            (
                "You are a senior software engineer mentor. "
                "Give ONE practical, actionable software engineering tip. "
                "It should be specific, useful for a student, and under 100 words. "
                "Topics can include: clean code, git, debugging, system design, "
                "algorithms, career, productivity, or tools."
            ),
            "Give me today's software engineering tip."
        )
    except Exception as e:
        return f"❌ AI Error: {str(e)}"


async def analyze_image(file_path: str, prompt: str = None) -> str:
    try:
        def _run():
            sample_file = client.files.upload(file=file_path)
            p = prompt or "Analyze this image. If it's an error, suggest a fix. If it's code, explain what it does."
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[p, sample_file]
            )
            return response.text
        return await asyncio.to_thread(_run)
    except Exception as e:
        return f"❌ Vision Error: {str(e)}"