from config import setting
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = setting.DB_URL

Engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= Engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()