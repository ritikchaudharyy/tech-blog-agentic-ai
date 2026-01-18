from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import os
from auth import resolve_role

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

OWNER_API_KEY = os.getenv("OWNER_API_KEY")


class LoginRequest(BaseModel):
    email: EmailStr
    api_key: str | None = None


class LoginResponse(BaseModel):
    role: str
    api_key: str


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    """
    Login endpoint for User & Admin.
    Admin requires OWNER_API_KEY.
    """

    role = resolve_role(payload.email, payload.api_key)

    # For now:
    # - Admin gets OWNER_API_KEY
    # - User gets a placeholder session key (upgrade later)
    if role == "admin":
        return {
            "role": "admin",
            "api_key": OWNER_API_KEY
        }

    return {
        "role": "user",
        "api_key": "user-session-key"
    }
