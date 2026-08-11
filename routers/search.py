# 담당: 준모 - 검색 + 태그 필터링 (핵심 기능)
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search_posts(
    board_id: int = Query(...),
    keyword: str | None = Query(None, min_length=1, max_length=50),
    tags: list[str] = Query([]),
    db: Session = Depends(get_db),
):
    # TODO(준모): 검색 + 태그 필터
    #  - keyword: 제목 OR 본문에 포함 (공백만 입력은 400)
    #  - tags: 선택된 태그를 가진 게시글만 (다중 선택 가능)
    #  - keyword와 tags 둘 다 있으면 AND 조건
    #  - 결과는 하은의 PostListItem 목록으로 반환
    #  - 결과 없으면 빈 배열 (프론트에서 "검색 결과가 없습니다" 표시)
    raise NotImplementedError
