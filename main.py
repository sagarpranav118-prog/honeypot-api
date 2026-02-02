from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import re
from typing import List, Dict

# ---------------- APP CONFIG ----------------

app = FastAPI(
    title="Honeypot Agentic Scam Intelligence API",
    description="An agentic honeypot system that detects scams, extracts indicators, and strategically engages scammers.",
    version="1.0.0"
)

API_KEY = "my_secret_key"


# ---------------- DATA MODEL ----------------

class Message(BaseModel):
    message: str


# ---------------- HEALTH CHECK ----------------

@app.get("/")
def health():
    return {
        "status": "active",
        "service": "Honeypot Agentic Scam Intelligence API"
    }


# ---------------- EXTRACTION ENGINE ----------------

def extract_phone_numbers(text: str) -> List[str]:
    # Indian phone number pattern
    return re.findall(r"\b[6-9]\d{9}\b", text)


def extract_upi_ids(text: str) -> List[str]:
    return re.findall(r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b", text)


def extract_urls(text: str) -> List[str]:
    return re.findall(r"https?://[^\s]+", text)


# ---------------- SCAM CONFIDENCE ENGINE ----------------

def calculate_scam_score(text: str) -> int:
    indicators = {
        "lottery": 25,
        "winner": 20,
        "prize": 20,
        "free": 10,
        "urgent": 15,
        "click": 10,
        "limited": 10,
        "congratulations": 15,
        "claim": 10,
        "offer": 10
    }

    score = 0
    text = text.lower()

    for keyword, weight in indicators.items():
        if keyword in text:
            score += weight

    return min(score, 100)


# ---------------- AGENTIC REASONING BRAIN ----------------

def agentic_persona_decision(
    scam_score: int,
    extracted: Dict[str, List[str]]
) -> Dict[str, str]:
    """
    Multi-step agentic reasoning:
    Decides the best next psychological move.
    """

    if scam_score < 30:
        return {
            "stage": "benign_analysis",
            "reply": "Thank you for the message. I will review the details carefully."
        }

    if 30 <= scam_score < 60:
        if not extracted["phone_numbers"]:
            return {
                "stage": "trust_building",
                "reply": "This sounds interesting. Can we talk on a call? Please share your number."
            }
        return {
            "stage": "engagement",
            "reply": "Okay, please explain the next steps to proceed."
        }

    # HIGH CONFIDENCE SCAM (>= 60)

    if not extracted["phone_numbers"]:
        return {
            "stage": "extract_phone",
            "reply": "I am very interested. Please share your contact number."
        }

    if not extracted["upi_ids"]:
        return {
            "stage": "extract_upi",
            "reply": "I tried to make the payment, but it failed. Please share your UPI ID."
        }

    if not extracted["urls"]:
        return {
            "stage": "extract_url",
            "reply": "Please send the official website or payment link for verification."
        }

    return {
        "stage": "stalling",
        "reply": "Thank you. I am verifying all details. Please wait."
    }


# ---------------- MAIN ENDPOINT ----------------

@app.post("/honeypot")
def honeypot(
    data: Message,
    authorization: str = Header(None, alias="Authorization")
):
    # Authentication
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Scam analysis
    scam_score = calculate_scam_score(data.message)
    is_scam = scam_score >= 30

    # Entity extraction
    extracted_data = {
        "phone_numbers": extract_phone_numbers(data.message),
        "upi_ids": extract_upi_ids(data.message),
        "urls": extract_urls(data.message)
    }

    # Agentic reasoning
    persona_output = agentic_persona_decision(
        scam_score,
        extracted_data
    )

    # Final response
    return {
        "is_scam": is_scam,
        "scam_confidence_score": scam_score,
        "received_message": data.message,
        "extracted_indicators": extracted_data,
        "agentic_stage": persona_output["stage"],
        "agentic_persona_reply": persona_output["reply"]
    }
