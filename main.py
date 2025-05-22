from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import SessionLocal
from models import Base, SenseData
from database import engine
import traceback
from routes import auth, admin

app = FastAPI()

# 라우터 등록
app.include_router(auth.router) # 꼭 있어야 함
app.include_router(admin.router)


# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.208:3000"],  # 필요한 경우 프론트 주소로 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB 테이블 생성
Base.metadata.create_all(bind=engine)

# ✅ 입력 모델 정의
class SenseInput(BaseModel):
    date: str
    location: str
    sense_type: str
    keyword: str
    emotion_score: float
    description: str

# ✅ 기록 추가 API
@app.post("/records")
def create_record(data: SenseInput):
    db = SessionLocal()
    try:
        record = SenseData(**data.dict())
        db.add(record)
        db.commit()
        db.refresh(record)
        return {"message": "등록 완료", "id": record.id}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        db.close()

# ✅ 기록 조회 API
@app.get("/records")
def get_records():
    db = SessionLocal()
    try:
        records = db.query(SenseData).all()
        return [
            {
                "id": r.id,
                "date": r.date or "",
                "location": r.location or "",
                "sense_type": r.sense_type or "",
                "keyword": r.keyword or "",
                "emotion_score": float(r.emotion_score or 0),  # 반드시 float!
                "description": r.description or ""
            }
            for r in records
        ]
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        db.close()

