from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import re

app = FastAPI(title="Honeypot Scam Detection API")

API_KEY = "my_secret_key"

# ---------- REQUEST MODELS (MATCH HACKATHON) ----------

class IncomingMessage(BaseModel):
    sender: str
    text: str
    timestamp: int

class IncomingRequest(BaseModel):
    sessionId: str
    message: IncomingMessage
    conversationHistory: List[Dict]
    metadata: Dict


# ---------- SCAM LOGIC ----------

def scam_confidence_score(text: str) -> int:
    keywords = {
        "bank": 20,
        "blocked": 20,
        "verify": 20,
        "urgent": 15,
        "account": 15,
        "click": 10,
        "immediately": 15
    }
    score = 0
    text = text.lower()
    for k, w in keywords.items():
        if k in text:
            score += w
    return min(score, 100)


def agentic_reply(score: int) -> str:
    if score < 30:
        return "Thanks for the information. I will check and respond."
    if score < 60:
        return "Can you explain why this verification is needed?"
    return "Why is my account being suspended?"


# ---------- MAIN ENDPOINT (WHAT JUDGES HIT) ----------

@app.post("/")
def honeypot_root(
    data: IncomingRequest,
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = data.message.text
    score = scam_confidence_score(text)
    reply = agentic_reply(score)

    return {
        "status": "success",
        "reply": reply
    }
