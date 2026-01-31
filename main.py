from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

API_KEY = "my_secret_key"

class MessageInput(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "active", "message": "Honeypot API is running"}

@app.post("/honeypot")
def honeypot(data: MessageInput, authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    msg = data.message.lower()

    if "won" in msg or "lottery" in msg or "prize" in msg:
        return {
            "is_scam": True,
            "scam_type": "Lottery Scam",
            "reason": "Message promises reward"
        }

    return {
        "is_scam": False,
        "scam_type": "None",
        "reason": "No scam patterns detected"
    }
