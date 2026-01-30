from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

API_KEY = "my_secret_key"

@app.get("/")
def root():
    return {"status": "active", "message": "Honeypot API is running"}

@app.get("/honeypot")
def honeypot(authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "status": "ok",
        "message": "Honeypot endpoint reached successfully"
    }