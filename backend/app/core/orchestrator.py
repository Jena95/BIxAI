from app.services.ai_client import GeminiClient
from app.services.bigquery_client import BigQueryClient

class AnalyticsOrchestrator:
    def __init__(self, project_id: str, dataset: str, table: str):
        self.gemini = GeminiClient()
        self.bq = BigQueryClient(project_id=project_id)
        self.project_id = project_id
        self.dataset = dataset
        self.table = table

    def handle_question(self, question: str):
        prompt = (
            f"Generate a valid BigQuery SQL query that answers this question: \"{question}\".\n"
            f"Use the table `{self.project_id}.{self.dataset}.{self.table}`.\n"
            f"Only return the SQL query, no explanations."
        )
        sql = self.gemini.ask(prompt)
        results = self.bq.run_query(sql)

        return {
            "sql": sql,
            "results": results
        }
