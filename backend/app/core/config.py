from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GearGap API"
    ENVIRONMENT: str = "local"

    # Database (Supabase PostgreSQL)
    DATABASE_URL: str = "postgresql+psycopg://postgres:password@localhost:5432/geargap"

    # Blizzard API (Battle.net)
    BLIZZARD_CLIENT_ID: str = ""
    BLIZZARD_CLIENT_SECRET: str = ""
    BLIZZARD_REGION: str = "kr"
    BLIZZARD_NAMESPACE: str = "profile-kr"
    BLIZZARD_LOCALE: str = "en_US"

    # Character cache TTL (seconds)
    CHARACTER_CACHE_TTL: int = 600  # 10 minutes

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "https://geargap.app",
        "https://gear-gap-two.vercel.app",
    ]

    # Admin
    ADMIN_API_KEY: str = ""

    # Phase 2
    ANTHROPIC_API_KEY: str = ""


settings = Settings()
