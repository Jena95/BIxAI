# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(
    title="Natural Language Analytics API",
    version="0.1.0"
)

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://5173-cs-d9f0ebd2-9b75-4534-8070-65868fb45d2a.cs-asia-southeast1-seal.cloudshell.dev"],  # You can replace * with your frontend URL for more security , allow_origins=["https://5173-<your-project>.cloudshell.dev"]

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")
