from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from services.ai_client import GeminiClient
from core.orchestrator import AnalyticsOrchestrator
from middleware.auth import get_current_user
import traceback    # For detailed error logging

import os

router = APIRouter()

gemini = GeminiClient()

class QueryRequest(BaseModel):
    question: str
    dataset: Optional[str] = None
    table: Optional[str] = None

class AskRequest(BaseModel):
    question: str

@router.get("/")
def root():
    return {"message": "API is up and running 🚀"}


@router.get("/secure")
def secure_endpoint(current_user: str = Depends(get_current_user)):
    return {"message": f"Welcome, user {current_user}!"}

@router.post("/ask")
def ask_question(payload: AskRequest, current_user: str = Depends(get_current_user)):
    try:
        answer = gemini.ask(payload.question)
        return {"question": payload.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_data(request: QueryRequest, current_user: str = Depends(get_current_user)):
    question = request.question
    project = os.getenv("GCP_PROJECT_ID", "brave-reason-421203")  # fallback to hardcoded if env var not set
    dataset = request.dataset or os.getenv("BIGQUERY_DATASET")
    table = request.table or os.getenv("BIGQUERY_TABLE")

    if not dataset or not table:
        raise HTTPException(status_code=400, detail="Dataset and table must be specified (in request or env vars)")

    try:
        orchestrator = AnalyticsOrchestrator(project, dataset, table)
        result = orchestrator.handle_question(question)
        return result

    except Exception as e:
        print("❌ ERROR in /query:", traceback.format_exc()) # Log the full traceback for debugging
        raise HTTPException(status_code=500, detail=str(e))

