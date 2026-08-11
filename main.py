# 공통 파일 - 라우터 등록까지 완성해뒀으니 이후 수정 금지
# 실행: uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models  # noqa: F401  (테이블 정의를 metadata에 등록)
from database import Base, engine
from routers import auth, boards, comments, posts, reactions, search

# 서버 시작 시 없는 테이블 자동 생성 (everytime.db)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Everytime Plus API")

# React 개발 서버에서의 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)       # 나희
app.include_router(comments.router)   # 나희
app.include_router(reactions.router)  # 나희
app.include_router(boards.router)     # 서현
app.include_router(posts.router)      # 하은
app.include_router(search.router)     # 준모


@app.get("/")
def health_check():
    return {"status": "ok"}
