# 담당: 준모 - 검색 + 태그 필터링 (핵심 기능)
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from auth_utils import get_current_user_optional
from database import get_db
from models import Board, Post, Tag, User
from post_utils import paginate_posts
from schemas.common import Page
from schemas.post import PostListItem

router = APIRouter(prefix="/search", tags=["search"])

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50


def normalize_tags(tags: list[str]) -> list[str]:
    """태그 쿼리를 정리한다.

    ?tags=시험&tags=과제 (키 반복) 형식이 기본이지만,
    ?tags=시험,과제 (콤마) 형식으로 보내는 클라이언트도 있어서 둘 다 받는다.
    """
    normalized = []
    for raw in tags:
        for name in raw.split(","):
            name = name.strip()
            if name and name not in normalized:
                normalized.append(name)
    return normalized


@router.get("", response_model=Page[PostListItem])
def search_posts(
    board_id: int = Query(...),
    keyword: str | None = Query(None, max_length=50),
    tags: list[str] = Query([]),
    page: int = Query(1, ge=1),
    size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    """
    - keyword와 tags를 동시에 지정하면 AND 조건으로 검색됨
    - keyword가 공백만 입력된 경우 400 에러 반환
    - 조건에 맞는 게시글이 없으면 빈 배열 반환
    - 정렬과 페이지 형태는 /boards/{id}/posts와 동일 (post_utils 공용)
    """

    # keyword가 공백만 입력된 건지 확인
    if keyword is not None and not keyword.strip():
        raise HTTPException(status_code=400, detail="검색어는 공백만 입력할 수 없습니다.")

    board = db.get(Board, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="게시판을 찾을 수 없습니다")

    query = db.query(Post).filter(Post.board_id == board_id)

    # keyword 필터링 (제목 + 본문)
    if keyword:
        query = query.filter(
            or_(Post.title.contains(keyword), Post.content.contains(keyword))
        )

    # tags 필터링 (선택한 태그를 모두 가진 글만 = AND)
    for tag_name in normalize_tags(tags):
        query = query.filter(Post.tags.any(Tag.name == tag_name))

    query = query.order_by(Post.created_at.desc(), Post.id.desc())

    return paginate_posts(query, page, size, user)
