# 담당: 준모 - 검색 + 태그 필터링 (핵심 기능)
from fastapi import APIRouter, Depends, Query, HTTPException
from models import Post, Tag
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from schemas.post import PostListItem

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[PostListItem])
def search_posts(
    board_id: int = Query(...),
    keyword: str | None = Query(None, min_length=1, max_length=50),
    tags: list[str] = Query([]),
    db: Session = Depends(get_db),
):
    # TODO(준모): 검색 + 태그 필터
    """
    - keyword와 tags를 동시에 지정하면 AND 조건으로 검색됨
    - keyword가 공백만 입력된 경우 400 에러 반환
    - 조건에 맞는 게시글이 없으면 빈 배열 반환
    """

    # keyword가 공백만 입력된 건지 확인
    if keyword and not keyword.strip():
        raise HTTPException(status_code=400, detail="검색어는 공백만 입력할 수 없습니다.")

    query = db.query(Post).filter(Post.board_id == board_id)

    # keyword 필터링
    if keyword:
        query = query.filter(or_(Post.title.contains(keyword), Post.content.contains(keyword)))

    # tags 필터링
    if tags:
        for tag_name in tags:
            query = query.filter(Post.tags.any(Tag.name == tag_name))

    posts = query.all()

    result = []
    for post in posts:
        result.append(PostListItem(
            id=post.id,
            title=post.title,
            content_preview=post.content[:100] + ("..." if len(post.content) > 100 else ""),
            tags=[tag.name for tag in post.tags],
            like_count=sum(1 for r in post.reactions if r.type == "like"),
            dislike_count=sum(1 for r in post.reactions if r.type == "dislike"),
            author_nickname="익명" if post.is_anonymous else post.author.nickname,
            created_at=post.created_at
        ))
    return result