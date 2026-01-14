from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.auth import verify_owner
from backend.services.newsletter_ai import generate_weekly_newsletter

router = APIRouter(
    prefix="/api/admin/newsletter",
    tags=["Newsletter"],
    dependencies=[Depends(verify_owner)]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/preview")
def preview_newsletter(db: Session = Depends(get_db)):
    return generate_weekly_newsletter(db)
