from pydantic_settings import BaseSettings , SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  

class Settings(BaseSettings):
    SQLALCHEMY_BASE_URL: str
    JWT_SECRET_KEY:str
    model_config = SettingsConfigDict(env_file=str(BASE_DIR/".env"))
    
    
settings=Settings()    