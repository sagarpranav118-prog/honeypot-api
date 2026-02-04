from fastapi import FastAPI, Header
from pydantic import BaseModel
import re
from typing import List, Optional

app = FastAPI()

# ================= CONFIG =================
API_KEY = "my_secret_key"

# ================= MODELS =================
class MessageContent(BaseModel):
    sender: str
    text: str
    timestamp: int

class Payload(BaseModel):
    sessionId: str
    message: MessageContent
    conversationHistory: List[dict] = []
    metadata: dict = {}

# ================= HELPERS =================
def extract_phone_numbers(text: str):
    return re.findall(r"\b[6-9]\d{9}\b", text)

def extract_upi_ids(text: str):
    return re.findall(r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b", text)

def extract_urls(text: str):
    return re.findall(r"https?://[^\s]+", text)

def detect_scam(text: str):
    keywords = [
        "account blocked", "verify immediately", "urgent",
        "lottery", "prize", "winner", "click", "suspended"
    ]
    text_lower = text.lower()
    return any(k in text_lower for k in keywords)

# ================= ROOT =================
@app.get("/")
def root():
    return {
        "status": "success",
        "reply": "Honeypot Scam Detection API is running"
    }

# ================= MAIN ENDPOINT =================
@app.post("/")
def honeypot(payload: Payload, x_api_key: Optional[str] = Header(None)):
    # ---- Auth Check ----
    if x_api_key != API_KEY:
        return {
            "status": "error",
            "reply": "Unauthorized"
        }

    text = payload.message.text

    phones = extract_phone_numbers(text)
    upis = extract_upi_ids(text)
    urls = extract_urls(text)
    is_scam = detect_scam(text)

    # ---- Agentic Persona Reply ----
    if is_scam:
        reply = (
            "I’m facing issues accessing my account. "
            "Can you explain the process clearly?"
        )
    else:
        reply = "Can you please provide more details?"

    return {
        "status": "success",
        "reply": reply,
        "analysis": {
            "is_scam": is_scam,
            "extracted_phone_numbers": phones,
            "extracted_upi_ids": upis,
            "extracted_urls": urls
        }
    }
