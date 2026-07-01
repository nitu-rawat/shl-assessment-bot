import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# कैटलॉग डेटा लोड करना
with open("catalog.json", "r") as f:
    CATALOG_DATA = json.load(f)

# Assignment Schema के मुताबिक Pydantic Models
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

# HEALTH CHECK ENDPOINT
@app.get("/health")
def health_check():
    return {"status": "ok"}

# MAIN CHAT ENDPOINT
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_message = request.messages[-1].content.lower()
    
    reply_text = "I understand you are looking for an assessment. Could you please specify the role, skills, or seniority level you are targeting?"
    recommendations_list = []
    end_of_conversation = False

    if "java" in user_message:
        reply_text = "Great! For a Java Developer, I highly recommend our Java Online Test to check core technical skills."
        recommendations_list.append(
            Recommendation(name="Java Online Test", url="https://www.shl.com/solutions/products/java-test/", test_type="K")
        )
        if "stakeholder" in user_message or "personality" in user_message or "mid" in user_message:
            reply_text += " Since the role involves working with stakeholders, I have also added the OPQ32r personality assessment."
            recommendations_list.append(
                Recommendation(name="OPQ32r", url="https://www.shl.com/solutions/products/opq32r/", test_type="P")
            )
        end_of_conversation = True

    elif "difference" in user_message or "compare" in user_message or "opq" in user_message:
        reply_text = "OPQ32r is a Personality test (P) that measures behavioral preferences. GSA is a Cognitive test (K) that measures problem-solving and general ability."
        recommendations_list = []
        end_of_conversation = False

    return ChatResponse(
        reply=reply_text,
        recommendations=recommendations_list,
        end_of_conversation=end_of_conversation
    )