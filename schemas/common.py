# 공통 파일 - 담당: 재윤 / 사용: 서현·하은·준모
# 목록 응답(페이지네이션)과 시간 직렬화처럼 여러 담당자가 함께 쓰는 스키마를 모아둔다.
from datetime import datetime, timezone
from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, PlainSerializer


def to_utc_iso(value: datetime) -> str:
    """타임존 정보를 붙여서 내려준다.

    DB에는 타임존 없는 UTC로 저장된다(models.utcnow). 그대로 응답하면
    브라우저가 "2026-08-19T04:26:23"을 로컬 시간으로 읽어버려서 한국 기준 9시간
    어긋난다. 그래서 UTC임을 명시한 ISO 8601 문자열로 바꿔서 내보낸다.
    """
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


# created_at 같은 응답 필드에 쓴다. datetime 대신 이 타입을 쓰면 위 규칙이 적용된다.
UtcDateTime = Annotated[datetime, PlainSerializer(to_utc_iso, return_type=str)]


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """목록 조회 공통 응답. 게시글 목록/검색이 같은 형태를 쓴다."""

    items: list[T]
    page: int  # 현재 페이지 (1부터 시작)
    size: int  # 한 페이지 크기
    total_pages: int
    total_elements: int  # 조건에 맞는 전체 개수
