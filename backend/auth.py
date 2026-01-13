import os
from fastapi import Header, HTTPException, status

OWNER_API_KEY = os.getenv("OWNER_API_KEY")

if not OWNER_API_KEY:
    raise RuntimeError("OWNER_API_KEY is not set in environment variables")


def verify_owner(
    x_api_key: str | None = Header(default=None, alias="x-api-key")
):
    """
    Owner authentication dependency.
    Requires header: x-api-key
    """

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
    """
    Determines user role based on email + API key
    """
    if email == "admin@example.com":
        if api_key != OWNER_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid owner API key"
            )
        return "admin"

    return "user"
