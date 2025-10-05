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
async def query_data(request: QueryRequest):
    question = request.question

    project = os.getenv("GCP_PROJECT_ID")
    dataset = request.dataset or os.getenv("BIGQUERY_DATASET")
    table = request.table or os.getenv("BIGQUERY_TABLE")

    if not dataset or not table:
        raise HTTPException(status_code=400, detail="Dataset and table must be specified")

    try:
        prompt = (
            f"Generate a valid BigQuery SQL query that answers this question: \"{question}\".\n"
            f"Use the table `{project}.{dataset}.{table}`."
        )
        sql = gemini.ask(prompt)

        results = bq_client.run_query(sql)

        return {"sql": sql, "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

