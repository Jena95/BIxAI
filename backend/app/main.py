# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.api.auth import router as auth_router


app = FastAPI(
    title="Natural Language Analytics API",
    version="0.1.0"
)

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with your frontend URL for more security , allow_origins=["https://5173-<your-project>.cloudshell.dev"]

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_router, prefix="/auth")
app.include_router(api_router, prefix="/api")
