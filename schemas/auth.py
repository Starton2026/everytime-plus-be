# 담당: 나희 - 로그인/회원가입 요청·응답 스키마
from pydantic import BaseModel, ConfigDict


class SignupRequest(BaseModel):
    nickname: str  # 10자 이하, 특수문자/공백 금지, 중복 불가
    username: str  # 4~20자, 영문+숫자만, 중복 불가
    password: str  # 8~64자, 공백 불가
    # TODO(나희): field_validator로 위 유효성 규칙 구현


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    nickname: str


class MeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # User ORM 객체를 바로 반환 가능하게

    id: int
    username: str
    nickname: str
