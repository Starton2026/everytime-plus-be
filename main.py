# 공통 파일 - 라우터 등록까지 완성해뒀으니 이후 수정 금지
# 실행: uvicorn main:app --reload
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models  # noqa: F401  (테이블 정의를 metadata에 등록)
from database import Base, engine
from routers import auth, boards, comments, posts, reactions, search, tags

# 서버 시작 시 없는 테이블 자동 생성 (everytime.db)
Base.metadata.create_all(bind=engine)

# Render 무료 플랜은 디스크가 유지되지 않아서, 서버가 잠들었다 깨어날 때마다
# everytime.db가 빈 파일로 다시 만들어진다. 그러면 게시판·계정·게시글이 모두 사라져
# 시크릿 모드처럼 저장된 로그인 정보가 없는 상태에서는 로그인조차 할 수 없다.
# 그래서 기동할 때마다 기본 데이터를 채워둔다. (이미 있으면 그대로 두므로 여러 번 실행해도 안전)
if os.getenv("SEED_ON_STARTUP", "1") != "0":
    from seed import seed

    seed(verbose=False)

app = FastAPI(title="Everytime Plus API")

# React 개발 서버에서의 요청 허용
# localhost와 127.0.0.1은 브라우저가 서로 다른 출처로 취급하므로 둘 다 넣어둔다.
DEV_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]


# 배포한 프론트는 Vercel에 올라가 있다. 프로덕션 주소와 미리보기(PR) 주소가 매번
# 달라서 하나하나 적을 수 없으므로 *.vercel.app 을 정규식으로 허용한다.
VERCEL_ORIGIN_REGEX = r"https://[a-zA-Z0-9-]+\.vercel\.app"


def allowed_origins() -> list[str]:
    """개발 서버 출처 + 환경 변수로 추가한 출처.

    Vercel 외의 주소로 배포하거나 특정 도메인만 열어주고 싶으면 코드를 고치지 않고
    ALLOWED_ORIGINS 환경 변수로 추가한다. 여러 개면 콤마로 구분한다.

        ALLOWED_ORIGINS=https://everytime-plus.vercel.app,https://example.com

    (Render라면 대시보드 > Environment 에 넣으면 된다)
    """
    raw = os.getenv("ALLOWED_ORIGINS", "")
    extra = [origin.strip().rstrip("/") for origin in raw.split(",") if origin.strip()]

    return DEV_ORIGINS + [origin for origin in extra if origin not in DEV_ORIGINS]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins(),
    allow_origin_regex=VERCEL_ORIGIN_REGEX,
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
app.include_router(tags.router)       # 재윤


@app.get("/")
def health_check():
    return {"status": "ok"}
