# sample_loader.py
from database import SessionLocal
from models import SenseData
from datetime import datetime, timedelta
import random

def load_sample_data():
    db = SessionLocal()

    # 이미 있으면 생략
    if db.query(SenseData).count() > 0:
        print("샘플 데이터 이미 존재")
        return

    sense_types = {
        "향": ["라벤더", "커피향", "비누향", "풀냄새", "나무향"],
        "맛": ["귤", "초콜릿", "막걸리", "딸기", "녹차"],
        "소리": ["파도소리", "새소리", "바람소리", "비소리", "잔잔한 음악"],
        "시각": ["노을", "바다", "푸른 숲", "달빛", "고요한 거리"]
    }

    locations = ["서울 성수동", "제주 서귀포", "부산 광안리", "강릉 안목해변", "양평 들판", "인천 차이나타운"]
    descriptions = [
        "은은하고 포근한 느낌",
        "상쾌하고 기분 좋은 향기",
        "달콤하면서도 깊은 여운",
        "청량한 느낌과 여유로움",
        "자연과 함께하는 순간"
    ]

    now = datetime.now()
    records = []

    for i in range(50):
        sense_type = random.choice(list(sense_types.keys()))
        keyword = random.choice(sense_types[sense_type])
        record = SenseData(
            date=(now - timedelta(days=i)).strftime("%Y-%m-%dT%H:%M"),
            location=random.choice(locations),
            sense_type=sense_type,
            keyword=keyword,
            emotion_score=random.randint(-3, 5),
            description=random.choice(descriptions)
        )
        records.append(record)

    db.bulk_save_objects(records)
    db.commit()
    print("샘플 데이터 50개 삽입 완료")
