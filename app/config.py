from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    webpage_name: str = "Nishant eAcadmy"
    DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ASCESS_TOKEN_EXPIRE_MINUTES: int
    TWILIO_ACC_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    
    class Config:
        env_nested_delimiter = "__"

setting = Settings(_env_file = os.path.join(os.getcwd(), "app/.env"))
