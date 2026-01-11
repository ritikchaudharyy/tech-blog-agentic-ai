from fastapi import FastAPI
from dotenv import load_dotenv
import logging

# =========================
# LOAD ENV VARIABLES FIRST
# =========================
load_dotenv()

# =========================
# DATABASE & MODELS
# =========================
from database import engine
import models

# =========================
# ROUTES
# =========================
from routes.public import router as public_router
from routes.owner import router as owner_router

# =========================
# SERVICES
# =========================
from services.scheduler import start_scheduler


# =========================
# LOGGING CONFIG
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================
# DATABASE INIT
# =========================
models.Base.metadata.create_all(bind=engine)


# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="Agentic AI Knowledge Platform",
    description="AI-powered blogging, auto-publishing & agentic workflows",
    version="1.0.0"
)


# =========================
# ROUTES REGISTER
# =========================
app.include_router(public_router)
app.include_router(owner_router)


# =========================
# STARTUP EVENT
# =========================
@app.on_event("startup")
def startup_event():
    try:
        start_scheduler()
        logger.info("Scheduler started successfully")
    except Exception as e:
        logger.error(f"Scheduler failed to start: {e}")


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "Backend is running",
        "message": "Public + Owner routes active"
    }
