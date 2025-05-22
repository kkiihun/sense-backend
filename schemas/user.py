from pydantic import BaseModel, EmailStr
from typing import Optional

# 요청용 스키마
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class TokenData(BaseModel):
    email: Optional[EmailStr] = None

# 응답용 스키마
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
