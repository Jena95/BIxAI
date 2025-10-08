from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services.user_auth import create_user, authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(payload: RegisterRequest):
    try:
        user = create_user(payload.email, payload.password)
        return {"message": "User registered", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # raise HTTPException(status_code=500, detail="Registration failed")
        raise HTTPException(status_code=500, detail=str(e))
        

@router.post("/login")
def login(payload: LoginRequest):
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": user["id"]})
    return {"access_token": token, "token_type": "bearer"}
