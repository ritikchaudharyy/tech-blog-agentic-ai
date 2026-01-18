from fastapi import FastAPI
from dotenv import load_dotenv
import logging
import os
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

load_dotenv(override=False)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

from database import engine, get_db_info
import models

from routes.public import router as public_router
from routes.owner import router as owner_router
from routes.auth import router as auth_router

from services.scheduler import start_scheduler

try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    db_info = get_db_info()
    logger.info(f"Database Info: {db_info}")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")
    raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Application starting up...")
    
    try:
        start_scheduler()
        logger.info("✅ Scheduler started successfully")
    except Exception as e:
        logger.exception(f"❌ Scheduler failed to start: {e}")
    
    logger.info("✅ Application startup complete")
    
    yield
    
    logger.info("🛑 Application shutting down...")
    logger.info("✅ Application shutdown complete")

app = FastAPI(
    title="Agentic AI Knowledge Platform",
    description="AI-powered blogging, auto-publishing & agentic workflows",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    FRONTEND_URL,
]

ALLOWED_ORIGINS = [origin for origin in ALLOWED_ORIGINS if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(public_router, tags=["Public"])
app.include_router(owner_router, tags=["Owner/Admin"])
app.include_router(auth_router, tags=["Authentication"])

@app.get("/", tags=["System"])
def root():
    return {
        "service": "Tech Blog Agentic AI",
        "status": "running",
        "version": "1.0.0",
        "message": "API is operational. Visit /docs for interactive documentation.",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
        }
    }

@app.get("/health", tags=["System"])
def health_check():
    try:
        db_info = get_db_info()
        
        return {
            "status": "healthy",
            "service": "tech-blog-backend",
            "version": "1.0.0",
            "database": {
                "status": "connected",
                "type": db_info.get("database_type", "unknown"),
                "url": db_info.get("database_url", "unknown"),
            },
            "scheduler": "active",
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "tech-blog-backend",
            "error": str(e)
        }

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Tech Blog Agentic AI - Backend Server")
    logger.info("=" * 60)
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Database: {get_db_info().get('database_type', 'unknown')}")
    logger.info(f"CORS Origins: {ALLOWED_ORIGINS}")
    logger.info("=" * 60)