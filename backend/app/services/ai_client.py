import os
import requests

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

    def ask(self, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "key": self.api_key
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

        response = requests.post(self.api_url, headers=headers, params=params, json=data)

        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code}, {response.text}")

        result = response.json()
        try:
            return result['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            raise Exception("Failed to parse Gemini API response.")
