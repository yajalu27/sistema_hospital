import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import AnyUrl, EmailStr, Field


load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    #Configuracion de email
    EMAIL_FROM: EmailStr = Field(default="no-reply@example.com", env="EMAIL_FROM")
    SMTP_HOST: str = Field(default="localhost", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(default="", env="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    ENABLE_EMAIL: bool = Field(default=False, env="ENABLE_EMAIL")
    

    class Config:
        env_file = ".env"

settings = Settings()

# Validación manual opcional
if not settings.DATABASE_URL:
    raise ValueError("❌ Faltan variables obligatorias en el archivo .env")
