from pydantic import BaseModel, EmailStr

# 요청용 스키마
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 응답용 스키마
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
