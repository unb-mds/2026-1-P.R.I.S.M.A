# backend/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Prisma Insight API"
    API_V1_STR: str = "/api/v1"

    # Variáveis mapeadas do .env
    GITHUB_TOKEN: str
    PROJECT_OWNER: str = "unb-mds"
    PROJECT_REPO: str = "2026-1-P.R.I.S.M.A"

    # Configuração para ler o arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
