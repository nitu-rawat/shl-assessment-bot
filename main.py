import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI

app = FastAPI()

# 1. अपनी OpenAI API Key यहाँ सेट करें (या Environment Variable का उपयोग करें)
# बेहतर होगा कि आप इसे 'your-api-key' की जगह अपनी असली की से बदलें
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY_HERE"
client = OpenAI()

# 2. कैटलॉग डेटा लोड करना
with open("catalog.json", "r") as f:
    CATALOG_DATA = json.load(f)

# 3. Request और Response के लिए Pydantic Models (असाइनमेंट के नियमों के मुताबिक)
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool

# 4. HEALTH CHECK ENDPOINT
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 5. MAIN CHAT ENDPOINT
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    
    # सिस्टम प्रॉम्ट: इसमें हम AI को उसका रोल और कैटलॉग डेटा समझा रहे हैं
    system_prompt = f"""
    You are an expert SHL Assessment Recommendation Agent.
    Your goal is to guide recruiters from a vague hiring need to a specific list of 1-10 assessments from the SHL Catalog.

    CRITICAL RULES:
    1. ONLY recommend assessments present in the provided Catalog. NEVER make up a test or URL.
    2. If the user's request is vague (e.g., "I need a test"), DO NOT recommend anything yet. Ask clarifying questions (e.g., role, skills, seniority).
    3. If the user asks for comparison or refinement, handle it intelligently using the context.
    4. You must ALWAYS reply in a strict JSON format matching this schema:
    {{
       "reply": "Your conversational response to the user here.",
       "recommendations": [
          {{"name": "Test Name", "url": "Exact URL from catalog", "test_type": "K or P"}}
       ],
       "end_of_conversation": true/false
    }}
    Set "recommendations" as an empty array [] if you are still asking questions.
    Set "end_of_conversation" to true ONLY when final recommendations are provided and the task is complete.

    Here is the exact SHL Catalog you must use:
    {json.dumps(CATALOG_DATA, indent=2)}
    """

    # बातचीत का इतिहास (History) तैयार करना
    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in request.messages:
        api_messages.append({"role": msg.role, "content": msg.content})

    try:
        # LLM से JSON मोड में रिपॉन्स मांगना
        response = client.chat.completions.create(
            model="gpt-4o-mini", # या gpt-3.5-turbo / gpt-4o
            messages=api_messages,
            response_format={"type": "json_object"}
        )
        
        # AI के जवाब को पार्स (Parse) करना
        ai_response_content = response.choices[0].message.content
        result = json.loads(ai_response_content)
        
        return ChatResponse(
            reply=result.get("reply", ""),
            recommendations=result.get("recommendations", []),
            end_of_conversation=result.get("end_of_conversation", False)
        )
        
    except Exception as e:
        # अगर कोई गड़बड़ हो तो सेफ डिफ़ॉल्ट रिस्पॉन्स
        return ChatResponse(
            reply="I encountered an error processing your request. Could you please rephrase?",
            recommendations=[],
            end_of_conversation=False
        )