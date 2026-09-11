import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Roblox AI Script Assistant")

# এখানে তোমার আসল Gemini API Key বসাও
GEMINI_API_KEY = "AQ.Ab8RN6Jo6nLRMdg_uAIivOZZvnLeNWXzFHDx7lS1nmqURMxV9A"
genai.configure(api_key=GEMINI_API_KEY)


class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
async def generate_script(data: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-3.6-flash")

        system_instruction = (
            "You are a Roblox Luau expert. "
            "Return ONLY valid Luau script code. "
            "Do NOT include explanations, markdown formatting, or triple backticks like ```lua."
        )

        full_prompt = f"{system_instruction}\n\nTask: {data.prompt}"
        response = model.generate_content(full_prompt)

        clean_code = (
            response.text.replace("```lua", "").replace("```", "").strip()
        )

        return {"success": True, "script": clean_code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))