"""
RegRadar — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.api.routes import auth, business_profiles, compliance, alerts, documents, ca_dashboard

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    setup_logging()
    logger.info("RegRadar API starting up", env=settings.APP_ENV)
    yield
    logger.info("RegRadar API shutting down")


app = FastAPI(
    title="RegRadar API",
    description=(
        "MSME Regulatory Intelligence Platform — "
        "Monitors Indian regulatory changes and delivers personalised compliance alerts."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ───────────────────────────────────────────────────────────
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(
    business_profiles.router,
    prefix="/api/v1/profiles",
    tags=["Business Profiles"],
)
app.include_router(
    compliance.router,
    prefix="/api/v1/compliance",
    tags=["Compliance Items"],
)
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(
    documents.router, prefix="/api/v1/documents", tags=["Documents"]
)
app.include_router(
    ca_dashboard.router, prefix="/api/v1/ca", tags=["CA Dashboard"]
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "environment": settings.APP_ENV,
    }
