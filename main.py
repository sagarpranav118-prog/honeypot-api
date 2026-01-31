from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

API_KEY = "my_secret_key"

class Message(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "active", "message": "Honeypot API is running"}

@app.post("/honeypot")
def honeypot(data: Message, authorization: str = Header(None, alias="Authorization")):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    scam_keywords = ["lottery", "prize", "winner", "free money", "urgent", "click"]
    msg = data.message.lower()

    is_scam = any(word in msg for word in scam_keywords)

    return {
        "is_scam": is_scam,
        "received_message": data.message
    }
