from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 기존 Sensedata 모델 그대로 유지
class SenseData(Base):
    __tablename__ = "sensedata"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    location = Column(String, nullable=False)
    sense_type = Column(String, nullable=False)
    keyword = Column(String, nullable=False)
    emotion_score = Column(Float, nullable=False)
    description = Column(String, nullable=True)

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Colum(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)