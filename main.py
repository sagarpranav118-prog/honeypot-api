from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import re
from typing import List

app = FastAPI()

API_KEY = "my_secret_key"

class Message(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "active", "message": "Honeypot API is running"}

def extract_phones(text: str) -> List[str]:
    pattern = r'(\+91[\s-]?\d{10}|\b\d{10}\b)'
    return list(set(re.findall(pattern, text)))

def extract_urls(text: str) -> List[str]:
    pattern = r'(https?://[^\s]+)'
    return list(set(re.findall(pattern, text)))

def extract_upi(text: str) -> List[str]:
    pattern = r'[\w.\-]{2,}@[a-zA-Z]{2,}'
    return list(set(re.findall(pattern, text)))

@app.post("/honeypot")
def honeypot(
    data: Message,
    authorization: str = Header(None, alias="Authorization")
):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    msg_lower = data.message.lower()

    scam_keywords = [
        "lottery", "prize", "winner", "free money",
        "urgent", "click", "limited time", "offer"
    ]

    is_scam = any(word in msg_lower for word in scam_keywords)

    phones = extract_phones(data.message)
    urls = extract_urls(data.message)
    upi_ids = extract_upi(data.message)

    return {
        "is_scam": is_scam,
        "phones": phones,
        "urls": urls,
        "upi_ids": upi_ids,
        "received_message": data.message
    }
