# 담당: 나희 - 좋아요/싫어요 스키마 (게시글/댓글 공용)
from typing import Literal

from pydantic import BaseModel


class ReactionRequest(BaseModel):
    type: Literal["like", "dislike"]


class ReactionResponse(BaseModel):
    like_count: int
    dislike_count: int
    my_reaction: Literal["like", "dislike"] | None  # 내가 누른 상태 (없으면 None)
