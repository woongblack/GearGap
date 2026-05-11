from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine
from tenacity import retry, stop_after_attempt, wait_fixed

from app.core.config import settings

engine = create_engine(str(settings.DATABASE_URL))


def init_db() -> None:
    # Tables are created via Alembic migrations.
    # This import ensures all models are registered before metadata is used.
    from app.models import character, item, meta, patch, simulation  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def check_db_connection() -> None:
    with Session(engine) as session:
        session.exec(text("SELECT 1"))
