# 공통 파일 - 수정 금지 (변경 필요하면 팀 합의 후)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite: 프로젝트 폴더에 everytime.db 파일 하나로 동작
SQLALCHEMY_DATABASE_URL = "sqlite:///./everytime.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite + FastAPI 조합에 필요
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """라우터에서 Depends(get_db)로 DB 세션을 주입받는다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
