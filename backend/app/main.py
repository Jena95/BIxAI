from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_client import GeminiClient
from app.services.bigquery_client import BigQueryClient
import os

router = APIRouter()

bq_client = BigQueryClient(project_id=os.getenv("GCP_PROJECT_ID"))
gemini_client = GeminiClient()

class QueryRequest(BaseModel):
    question: str

@router.post("/api/query")
async def query_data(request: QueryRequest):
    question = request.question

    try:
        # Step 1: Generate SQL from Gemini
        sql = gemini_client.generate_sql(question)

        # Step 2: Run SQL on BigQuery
        results = bq_client.run_query(sql)

        return {
            "sql": sql,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))