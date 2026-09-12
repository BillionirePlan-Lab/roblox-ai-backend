import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Roblox AI Script Assistant")

# আসল API Key গোপন রাখতে Environment Variable ব্যবহার করা হচ্ছে
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_script(data: PromptRequest):
    try:
        # জটিল কোডিংয়ের জন্য গুগলের সেরা মডেল Pro ব্যবহার করা হয়েছে
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        system_instruction = (
            "You are a Roblox Luau expert. "
            "Return ONLY valid Luau script code. "
            "Do NOT include explanations, markdown formatting, or triple backticks like ```lua. "
            "CRITICAL: Always generate code for a Server Script. Do NOT use RunService.RenderStepped."
        )
        
        full_prompt = f"{system_instruction}\n\nTask: {data.prompt}"
        response = model.generate_content(full_prompt)
        
        clean_code = (
            response.text.replace("```lua", "").replace("```", "").strip()
        )
        
        return {"success": True, "script": clean_code}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
