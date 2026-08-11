# 공통 파일 - 담당: 나희 / 사용: 전원
# 비밀번호 해싱, JWT 발급/검증, 로그인 사용자 확인(get_current_user)
#
# 다른 팀원 사용법: 라우터 함수 파라미터에 아래처럼 추가하면
# 토큰 검증 + 사용자 조회까지 자동으로 된다.
#
#   from auth_utils import get_current_user
#
#   @router.post("/posts")
#   def create_post(..., user: User = Depends(get_current_user)):
#       ...  # user = 로그인한 User 객체. 토큰이 없거나 만료면 자동으로 401 응답
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from models import User

# 미니 프로젝트라 코드에 두지만, 배포 시엔 환경변수로 빼는 게 안전
SECRET_KEY = "everytime-plus-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24시간

bearer_scheme = HTTPBearer()
bearer_scheme_optional = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Authorization: Bearer <token> 헤더를 검증하고 User 객체를 반환한다."""
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="로그인이 필요합니다",
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise unauthorized

    user = db.get(User, int(payload["sub"]))
    if user is None:
        raise unauthorized
    return user


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme_optional),
    db: Session = Depends(get_db),
) -> User | None:
    """토큰이 없거나 유효하지 않으면 None. 비로그인도 볼 수 있는 목록/상세 조회에서
    is_mine, my_reaction 같은 "내 상태" 표시용으로 사용한다."""
    if credentials is None:
        return None
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
    return db.get(User, int(payload["sub"]))
