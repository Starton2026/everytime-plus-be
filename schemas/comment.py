# 담당: 나희 - 댓글 스키마
from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str  # 1~300자
    is_anonymous: bool = False


class CommentResponse(BaseModel):
    id: int
    content: str
    is_anonymous: bool
    author_nickname: str  # is_anonymous=True면 "익명"으로 내려주기
    like_count: int
    dislike_count: int
    created_at: datetime
    # TODO(나희): 프론트에서 수정/삭제 버튼 표시용 is_mine 필드 검토
