"""
RegRadar — Celery Application
Section 6, Component 3: Processing queue using Redis + Celery.
"""

from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "regradar",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    # Rate limiting for LLM API calls (Section 8)
    task_default_rate_limit="50/h",
    # Retry settings
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Auto-discover tasks from the tasks module
celery_app.autodiscover_tasks(["app.tasks"])
