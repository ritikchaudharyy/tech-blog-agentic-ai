from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./articles.db")

is_sqlite = DATABASE_URL.startswith("sqlite")

engine_config = {
    "echo": os.getenv("DB_ECHO", "false").lower() == "true",
}

if is_sqlite:
    engine_config["connect_args"] = {"check_same_thread": False}
    if ":memory:" in DATABASE_URL:
        engine_config["poolclass"] = StaticPool
else:
    engine_config["pool_pre_ping"] = True
    engine_config["pool_size"] = int(os.getenv("DB_POOL_SIZE", "5"))
    engine_config["max_overflow"] = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    engine_config["pool_recycle"] = 3600

engine = create_engine(DATABASE_URL, **engine_config)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)

def get_db_info():
    return {
        "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL.split("///")[-1],
        "database_type": "sqlite" if is_sqlite else "postgresql",
        "pool_size": engine.pool.size() if hasattr(engine.pool, 'size') else "N/A",
    }