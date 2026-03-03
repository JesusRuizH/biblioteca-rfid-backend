from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    POCKETBASE_URL: str
    POCKETBASE_EMAIL: str
    POCKETBASE_PASSWORD: str
    POCKETBASE_URL_IMAGENES: str
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    SCHEDULER_ENABLED: bool = True


    class Config:
        env_file = ".env"

settings = Settings()
