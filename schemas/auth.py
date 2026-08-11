# 담당: 나희 - 로그인/회원가입 요청·응답 스키마
import re

from pydantic import BaseModel, ConfigDict, field_validator


class SignupRequest(BaseModel):
    nickname: str  # 10자 이하, 특수문자/공백 금지, 중복 불가
    username: str  # 4~20자, 영문+숫자만, 중복 불가
    password: str  # 8~64자, 공백 불가

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, v: str) -> str:
        if not (1 <= len(v) <= 10):
            raise ValueError("닉네임은 1~10자여야 합니다")
        if not re.fullmatch(r"[가-힣a-zA-Z0-9]+", v):
            raise ValueError("닉네임에 특수문자와 공백은 사용할 수 없습니다")
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9]{4,20}", v):
            raise ValueError("아이디는 4~20자의 영문과 숫자만 사용할 수 있습니다")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not (8 <= len(v) <= 64):
            raise ValueError("비밀번호는 8~64자여야 합니다")
        if " " in v:
            raise ValueError("비밀번호에 공백은 사용할 수 없습니다")
        return v


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
