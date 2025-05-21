# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:MyPassWord12@localhost/sense_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  종속석 주입용
def get_db();
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()