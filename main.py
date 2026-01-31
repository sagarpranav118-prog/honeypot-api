from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import re
from typing import List, Dict

app = FastAPI()

API_KEY = "my_secret_key"

class Message(BaseModel):
    message: str


# ---------- EXTRACTION FUNCTIONS ----------

def extract_phone_numbers(text: str) -> List[str]:
    return re.findall(r'\b\d{10}\b', text)


def extract_urls(text: str) -> List[str]:
    return re.findall(r'https?://\S+|www\.\S+', text)


def extract_upi_ids(text: str) -> List[str]:
    return re.findall(r'\b[a-zA-Z0-9.\-_]+@[a-zA-Z]+\b', text)


# ---------- ROOT ----------

@app.get("/")
def root():
    return {
        "status": "active",
        "message": "Honeypot API is running successfully"
    }


# ---------- MAIN HONEYPOT API ----------

@app.post("/honeypot")
def honeypot(
    data: Message,
    authorization: str = Header(None, alias="Authorization")
):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    scam_keywords = [
        "lottery", "prize", "winner", "free money", "urgent",
        "click", "verify", "account blocked", "bank",
        "payment", "upi", "offer", "limited time"
    ]

    message_lower = data.message.lower()
    is_scam = any(keyword in message_lower for keyword in scam_keywords)

    extracted_data: Dict[str, List[str]] = {
        "phone_numbers": extract_phone_numbers(data.message),
        "urls": extract_urls(data.message),
        "upi_ids": extract_upi_ids(data.message)
    }

    return {
        "is_scam": is_scam,
        "received_message": data.message,
        "extracted_data": extracted_data
    }
