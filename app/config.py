"""
Конфигурация приложения.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Safety OPO System"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Система идентификации опасностей и рисков "
        "при работах повышенной опасности на нефтегазовых объектах"
    )
    DATABASE_URL: str = "sqlite:///./ai_safety_opo.db"
    AI_CAMERA_COUNT: int = 4
    AI_DETECTION_INTERVAL_SEC: int = 5

    class Config:
        env_file = ".env"

settings = Settings()
