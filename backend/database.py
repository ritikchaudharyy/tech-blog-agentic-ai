from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# =========================
# DATABASE CONFIG
# =========================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./articles.db"
)

# =========================
# ENGINE
# =========================
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

# =========================
# SESSION
# =========================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================
# BASE MODEL
# =========================
Base = declarative_base()


# =========================
# DB DEPENDENCY (FastAPI)
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
