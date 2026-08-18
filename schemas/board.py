# 담당: 서현 - 게시판 스키마
from pydantic import BaseModel


class BoardResponse(BaseModel):
    """GET /boards 응답에 쓰이는 게시판 정보 스키마."""

    id: int
    name: str  # 자유 게시판 / 새내기 게시판 / 졸업생 게시판
