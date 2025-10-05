from fastapi import APIRouter, HTTPException
from app.services.ai_client import GeminiClient

router = APIRouter()

gemini = GeminiClient()

@router.get("/")
def root():
    return {"message": "API is up and running 🚀"}

@router.post("/ask")
def ask_question(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question' in payload")

    try:
        answer = gemini.ask(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
