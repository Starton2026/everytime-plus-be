# 담당: 나희 - 댓글 스키마
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator


class CommentCreate(BaseModel):
    content: str  # 1~300자
    is_anonymous: bool = False

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not (1 <= len(v) <= 300):
            raise ValueError("댓글은 1~300자여야 합니다")
        return v


class CommentResponse(BaseModel):
    id: int
    content: str
    is_anonymous: bool
    author_nickname: str  # is_anonymous=True면 "익명"
    like_count: int
    dislike_count: int
    created_at: datetime
    is_mine: bool  # 프론트에서 삭제 버튼 표시용
    my_reaction: Literal["like", "dislike"] | None  # 내가 누른 좋아요/싫어요 상태
