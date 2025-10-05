from google.cloud import bigquery

class BigQueryClient:
    def __init__(self, project_id: str):
        self.client = bigquery.Client(project=project_id)

    def run_query(self, sql: str):
        query_job = self.client.query(sql)
        results = query_job.result()  # Wait for query to finish

        # Convert results to list of dicts for easy JSON serialization
        rows = [dict(row.items()) for row in results]
        return rows
