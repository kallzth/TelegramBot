import os
from google import genai
from bot.core.config import GEMINI_API_KEY

# Initialize the Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_FILE = os.path.join(BASE_DIR, "knowledge_base.txt")

async def get_summary(text: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            config={"system_instruction": "You are an expert engineer. Summarize this text into clear bullet points."},
            contents=text, # Matches parameter 'text'
        )
        return response.text
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

async def generate_prompt(raw_idea: str) -> str:
    try:
        system_instruction = "You are an expert Prompt Engineer. Use the RTF framework."
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config={"system_instruction": system_instruction},
            contents=raw_idea, # FIXED: Now matches parameter 'raw_idea'
        )
        return response.text
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

async def suggest_commit(description: str) -> str:
    try:
        system_instruction = "Convert this to a professional Conventional Commit message."
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config={"system_instruction": system_instruction},
            contents=description, # Matches parameter 'description'
        )
        return response.text
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

async def analyze_error(log: str) -> str:
    try:
        system_instruction = "Analyze this error log and suggest 3 fix steps."
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config={"system_instruction": system_instruction},
            contents=log, # Matches parameter 'log'
        )
        return response.text
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

async def quick_explain(concept: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={"system_instruction": "Explain this technical concept simply in 2-3 sentences."},
            contents=concept,
        )
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Path to your knowledge base
KB_FILE = "bot/knowledge_base.txt"

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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config={"system_instruction": system_instruction},
            contents=f"Context: {context}\n\nQuestion: {query}",
        )
        return response.text
    except Exception as e:
        return f"❌ Search Error: {str(e)}"

def clear_kb_file():
    try:
        # Opening with "w" (write) mode clears the file content
        with open(KB_FILE, "w", encoding="utf-8") as f:
            f.write("") 
        print(f"DEBUG: Knowledge base at {KB_FILE} cleared.")
        return True
    except Exception as e:
        print(f"DEBUG: Failed to clear KB: {e}")
        return False

async def analyze_image(file_path: str, prompt: str = None) -> str:
    try:
        # 1. Upload the image to Gemini's storage
        sample_file = client.files.upload(file=file_path)
        
        # 2. Default prompt if the user didn't provide one
        if not prompt:
            prompt = "Analyze this image. If it's an error, suggest a fix. If it's code, explain what it does."

        # 3. Generate response
        response = client.models.generate_content(
            model="gemini-1.5-flash", # Use 1.5-flash for the most stable Vision support
            contents=[prompt, sample_file]
        )
        return response.text
    except Exception as e:
        return f"❌ Vision Error: {str(e)}"