import os
import requests

class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

    def ask(self, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        response = requests.post(self.api_url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(f"[Gemini API error] {response.status_code}: {response.text}")

        result = response.json()
        try:
            return result['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            raise Exception("Failed to parse Gemini API response.")
    
    def generate_sql(self, question: str) -> str:
        prompt = f"Generate a BigQuery SQL query that answers this question: \"{question}\""
        return self.ask(prompt)
