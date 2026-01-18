import os
from fastapi import APIRouter, Header, HTTPException, status

router = APIRouter(prefix="/auth", tags=["Auth"])

OWNER_API_KEY = os.getenv("OWNER_API_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

if not OWNER_API_KEY:
    raise RuntimeError("OWNER_API_KEY is not set in environment variables")


def verify_owner(
    x_api_key: str | None = Header(default=None, alias="x-api-key")
):
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="x-api-key header missing"
        )

    if x_api_key != OWNER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid owner API key"
        )

    return True


def resolve_role(email: str, api_key: str | None):
    if email == ADMIN_EMAIL:
        if api_key != OWNER_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid owner API key"
            )
        return "admin"

    return "user"


@router.post("/login")
def login(payload: dict):
    return {
        "message": "Login endpoint reached",
        "payload": payload
    }
