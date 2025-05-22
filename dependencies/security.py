from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas.user import TokenData
from utils.token import decode_access_token
import os

# 1-1) OAuth2 scheme 정의 (tokenUrl은 /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 1-2) JWT 설정 불러오기
SECRET_KEY = os.getenv("JWT_SECRET", "devsecret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == token_data.email).first()
    if not user:
        raise credentials_exception

    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.is_admin != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다"
        )
    return current_user
