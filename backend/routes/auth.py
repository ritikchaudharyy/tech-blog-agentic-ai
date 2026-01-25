from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import os
import secrets
import time

from auth import resolve_role

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

OWNER_API_KEY = os.getenv("OWNER_API_KEY")

# --------------------------------------------------
# Login Models
# --------------------------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    api_key: str | None = None


class LoginResponse(BaseModel):
    role: str
    api_key: str


# --------------------------------------------------
# Forgot / Reset Password Models
# --------------------------------------------------

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


# token -> (email, expiry)
RESET_TOKENS: dict[str, tuple[str, float]] = {}


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    """
    Login endpoint for User & Admin.
    Admin requires OWNER_API_KEY.
    """

    role = resolve_role(payload.email, payload.api_key)

    if role == "admin":
        if not OWNER_API_KEY:
            raise HTTPException(status_code=500, detail="OWNER_API_KEY not configured")

        return {
            "role": "admin",
            "api_key": OWNER_API_KEY
        }

    return {
        "role": "user",
        "api_key": "user-session-key"
    }


# --------------------------------------------------
# FORGOT PASSWORD
# --------------------------------------------------

@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest):
    token = secrets.token_urlsafe(32)
    expiry = time.time() + 15 * 60  # 15 minutes

    RESET_TOKENS[token] = (payload.email, expiry)

    reset_link = f"http://localhost:5173/reset-password?token={token}"

    # TODO: replace with real email sender
    print(f"[RESET LINK] {reset_link}")

    return {"message": "Reset link sent"}


# --------------------------------------------------
# RESET PASSWORD
# --------------------------------------------------

@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest):
    record = RESET_TOKENS.get(payload.token)

    if not record:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    email, expiry = record

    if time.time() > expiry:
        del RESET_TOKENS[payload.token]
        raise HTTPException(status_code=400, detail="Reset token expired")

    # TODO:
    # Update user password in database here
    # hash password before saving

    del RESET_TOKENS[payload.token]

    return {"message": "Password reset successful"}
