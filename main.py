import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Roblox AI Script Assistant")

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "Server is running successfully!"}

@app.post("/generate")
async def generate_script(data: PromptRequest):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"success": False, "error": "GEMINI_API_KEY missing in Render Environment"}
            
        # গুগলের অফিশিয়াল নতুন ক্লায়েন্ট
        client = genai.Client(api_key=api_key.strip())
        
        system_instruction = (
            "You are a Roblox Luau expert. "
            "Return ONLY valid Luau script code. "
            "Do NOT include explanations, markdown formatting, or triple backticks like ```lua. "
            "CRITICAL: Always generate code for a Server Script. Do NOT use RunService.RenderStepped."
        )
        
        full_prompt = f"{system_instruction}\n\nTask: {data.prompt}"
        
        # সর্বশেষ Gemini 2.0 Flash মডেল
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=full_prompt,
        )
        
        if not response.text:
            return {"success": False, "error": "Empty response received from Gemini"}
            
        clean_code = response.text.replace("```lua", "").replace("```", "").strip()
        return {"success": True, "script": clean_code}
        
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        return {"success": False, "error": str(e)}
