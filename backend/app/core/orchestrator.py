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
            f"Only return the SQL query — no explanations, no markdown, no triple backticks."
        )

        sql = self.gemini.ask(prompt).strip()

        # 🧹 Clean up markdown/code block if included
        if sql.startswith("```"):
            lines = sql.strip("`").strip().splitlines()
            if lines[0].strip().lower() == "sql":
                lines = lines[1:]  # Remove the first 'sql' line
            sql = "\n".join(lines).strip()

        results = self.bq.run_query(sql)

        return {
            "sql": sql,
            "results": results
        }
