from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    POCKETBASE_URL: str
    POCKETBASE_EMAIL: str
    POCKETBASE_PASSWORD: str
    POCKETBASE_URL_IMAGENES: str

    class Config:
        env_file = ".env"

settings = Settings()
