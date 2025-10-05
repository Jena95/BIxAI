from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_client import GeminiClient
from app.services.bigquery_client import BigQueryClient
import os

router = APIRouter()

gemini = GeminiClient()
bq_client = BigQueryClient(project_id=os.getenv("GCP_PROJECT_ID"))

class QueryRequest(BaseModel):
    question: str

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


@router.post("/query")
def query_data(request: QueryRequest):
    question = request.question

    try:
        # Step 1: Generate SQL from Gemini
        sql = gemini.generate_sql(question)  # You need to add generate_sql method in GeminiClient

        # Step 2: Run SQL on BigQuery
        results = bq_client.run_query(sql)

        return {
            "sql": sql,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
