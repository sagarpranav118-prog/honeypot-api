from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import re

app = FastAPI()

API_KEY = "my_secret_key"

class IncomingMessage(BaseModel):
    sender: str
    text: str
    timestamp: int

class RequestBody(BaseModel):
    sessionId: str
    message: IncomingMessage
    conversationHistory: list
    metadata: dict

@app.post("/")
def scam_api(
    payload: RequestBody,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = payload.message.text.lower()

    scam_keywords = ["bank", "blocked", "verify", "urgent", "lottery", "prize"]
    is_scam = any(k in text for k in scam_keywords)

    phones = re.findall(r"\b\d{10}\b", text)
    upis = re.findall(r"\b[\w.-]+@[\w.-]+\b", text)
    urls = re.findall(r"https?://\S+", text)

    reply = (
        "I’m having trouble accessing my account. Can you please explain the issue clearly?"
        if is_scam
        else "Thank you for the information."
    )

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
