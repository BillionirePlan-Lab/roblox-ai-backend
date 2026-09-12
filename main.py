import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Roblox AI Script Assistant")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_script(data: PromptRequest):
    try:
        # প্রতি রিকোয়েস্টে ফ্রেশভাবে API Key লোড করা হচ্ছে
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing!")
            
        genai.configure(api_key=api_key)
        
        # ফ্রি ও ফাস্ট সার্ভিস নিশ্চিত করতে flash মডেল ব্যবহার করা হয়েছে
        model = genai.GenerativeModel("gemini-1.5-flash")
        
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
        # আসল এররটি Render-এর Logs ট্যাবে দেখতে পাওয়ার জন্য প্রিন্ট করা হলো
        print(f"--- DETAILED ERROR: {str(e)} ---")
        raise HTTPException(status_code=500, detail=str(e))
