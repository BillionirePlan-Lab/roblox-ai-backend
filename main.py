import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel

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
            
        genai.configure(api_key=api_key.strip())
        
        # কাজ করবে এমন মডেলের নাম
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        system_instruction = (
            "You are a Roblox Luau expert. "
            "Return ONLY valid Luau script code. "
            "Do NOT include explanations, markdown formatting, or triple backticks like ```lua. "
            "CRITICAL: Always generate code for a Server Script. Do NOT use RunService.RenderStepped."
        )
        
        full_prompt = f"{system_instruction}\n\nTask: {data.prompt}"
        response = model.generate_content(full_prompt)
        
        if not response.text:
            return {"success": False, "error": "Empty response received from Gemini"}
            
        clean_code = response.text.replace("```lua", "").replace("```", "").strip()
        return {"success": True, "script": clean_code}
        
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        return {"success": False, "error": str(e)}
        
        if not response.text:
            return {"success": False, "error": "Empty response received from Gemini"}
            
        clean_code = response.text.replace("```lua", "").replace("```", "").strip()
        return {"success": True, "script": clean_code}
        
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        return {"success": False, "error": str(e)}
