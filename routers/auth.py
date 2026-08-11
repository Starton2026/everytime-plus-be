# 담당: 나희 - 로그인 / 회원가입
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from database import get_db
from models import User
from schemas.auth import MeResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(db: Session = Depends(get_db)):
    # TODO(나희): 회원가입
    #  - SignupRequest 받아서 유효성/중복 검사
    #  - hash_password()로 비밀번호 해싱 후 User 저장
    #  - 성공 시 create_access_token()으로 토큰 발급 (자동 로그인)
    #  - 실패 시 400 "이미 사용 중인 아이디입니다"
    raise NotImplementedError


@router.post("/login")
def login(db: Session = Depends(get_db)):
    # TODO(나희): 로그인
    #  - LoginRequest 받아서 verify_password()로 검증
    #  - 성공 시 TokenResponse 반환
    #  - 실패 시 401 "아이디 또는 비밀번호가 올바르지 않습니다"
    raise NotImplementedError


@router.get("/me", response_model=MeResponse)
def get_me(user: User = Depends(get_current_user)):
    """내 정보 조회. 프론트에서 앱 실행 시 토큰 유효성 확인용으로도 사용."""
    return user
