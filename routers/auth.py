# 담당: 나희 - 로그인 / 회원가입 / 내 정보
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth_utils import create_access_token, get_current_user, hash_password, verify_password
from database import get_db
from models import User
from schemas.auth import LoginRequest, MeResponse, SignupRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(body: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다")
    if db.query(User).filter(User.nickname == body.nickname).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 닉네임입니다")

    user = User(
        username=body.username,
        nickname=body.nickname,
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 회원가입 성공 시 자동 로그인 (토큰 바로 발급)
    return TokenResponse(access_token=create_access_token(user.id), nickname=user.nickname)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    if user is None or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다")

    return TokenResponse(access_token=create_access_token(user.id), nickname=user.nickname)


@router.get("/me", response_model=MeResponse)
def get_me(user: User = Depends(get_current_user)):
    """내 정보 조회. 프론트에서 앱 실행 시 토큰 유효성 확인용으로도 사용."""
    return user
