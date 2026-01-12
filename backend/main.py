from fastapi import FastAPI
from dotenv import load_dotenv
import logging

from fastapi.middleware.cors import CORSMiddleware

# =========================
# LOAD ENV VARIABLES FIRST
# =========================
load_dotenv()

# =========================
# LOGGING CONFIG
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
)
logger = logging.getLogger(__name__)

# =========================
# DATABASE & MODELS
# =========================
from backend.database import engine
from backend import models

# =========================
# ROUTES
# =========================
from backend.routes.public import router as public_router
from backend.routes.owner import router as owner_router

# =========================
# SERVICES
# =========================
from backend.services.scheduler import start_scheduler

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
# CORS CONFIG (Frontend Ready)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite / React
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    except Exception:
        logger.exception("Scheduler failed to start")

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "Backend is running",
        "message": "Public + Owner routes active"
    }
