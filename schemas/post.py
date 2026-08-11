# 담당: 하은 - 게시글 CRUD 스키마
from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str  # 1~100자, 공백만 입력 불가, 앞뒤 공백 자동 제거
    content: str  # 1~2000자
    tags: list[str] = []  # 최대 3개
    is_anonymous: bool = False
    # TODO(하은): field_validator로 유효성 규칙 구현


class PostUpdate(BaseModel):
    title: str
    content: str
    tags: list[str] = []


class PostListItem(BaseModel):
    """게시글 리스트용: 본문은 일부만"""

    id: int
    title: str
    content_preview: str
    tags: list[str]
    like_count: int
    dislike_count: int
    author_nickname: str  # is_anonymous=True면 "익명"
    created_at: datetime


class PostDetail(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]
    like_count: int
    dislike_count: int
    author_nickname: str
    is_anonymous: bool
    created_at: datetime
    # 댓글은 GET /posts/{id}/comments 로 따로 조회 (나희 담당과 겹치지 않게)
