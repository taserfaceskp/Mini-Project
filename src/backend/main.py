from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Multimodal AI Brand Spoofing and Credential Harvesting Phishing Detection Engine",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "ollama": True
    }

@app.post("/api/v1/analyze")
async def analyze_payload(
    email_text: str = Form(...),
    screenshot: UploadFile = File(...)
):
    return {
        "threat_score": 8.5,
        "brand_detected": "Microsoft",
        "domain_match": False,
        "urgency_score": 0.95,
        "explanation": "This is a mock endpoint response. The actual integrated ML analysis will run here in Week 5."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
