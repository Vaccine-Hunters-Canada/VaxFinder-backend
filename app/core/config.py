from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # -- Project Details ---
    PROJECT_NAME: str = "VaxFinder"
    PROJECT_DESCRIPTION: str = "RESTful APIs for VaxFinder."
    PROJECT_VERSION: str = "1.0.0"

    # -- Documentation ---
    OPENAPI_URL: Optional[str] = "/openapi.json"
    SWAGGER_URL: Optional[str] = "/swagger"
    REDOC_URL: Optional[str] = "/redoc"

    # -- API Versioning ---
    API_V1_STR: str = "/api/v1"

    # -- Database Connection ---
    DB_URL: str


settings = Settings()
