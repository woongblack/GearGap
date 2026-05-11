# Entry point for local development: uvicorn main:app --reload
# Production (Cloud Run): uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
from app.main import app  # noqa: F401
