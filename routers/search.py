# 담당: 준모 - 검색 + 태그 필터링 (핵심 기능)
from fastapi import APIRouter, Depends, Query, HTTPException
from models import Post, Tag
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from schemas.post import PostListItem

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search_posts(
    board_id: int = Query(...),
    keyword: str | None = Query(None, min_length=1, max_length=50),
    tags: list[str] = Query([]),
    db: Session = Depends(get_db),
):
    # TODO(준모): 검색 + 태그 필터
    #  - 결과는 하은의 PostListItem 목록으로 반환
    #  - 결과 없으면 빈 배열 (프론트에서 "검색 결과가 없습니다" 표시)     => 결과가 없으면 = [] 빈배열 표시됨 ? 프론트
    #  - keyword: 제목 OR 본문에 포함 (공백만 입력은 400)             => 공백입력시 -> 400 에러 및 "검색어는 공백만 입력할 수 없습니다." 메시지 반환
    #  - keyword와 tags 둘 다 있으면 AND 조건                       => and 조건으로 묶여서 검색됨
    #  - tags: 선택된 태그를 가진 게시글만 (다중 선택 가능)
        #   [테스트 과정] : [결과]
        # 1. borad_id=1, keyword=none, tags=none : 게시판 1번의 모든 글 -> 첫 번째 테스트 글 나옴
        # 2. borad_id=1, keyword="테스트", tags=none : 게시판 1번의 제목/본문에 "테스트" 포함 글 -> 첫 번째 테스트 글 나옴
        # 3. borad_id=1, keyword="asd23", tags=none : 게시판 1번의 제목/본문에 "asd23" 포함 글 -> 없음 안나옴
        # 4. borad_id=1, keyword=none, tags=["시험"] : 게시판 1번의 "시험" 태그 글 -> 첫 번째 테스트 글 나옴 
        # 5. borad_id=1, keyword=none, tags=["과제"] : 게시판 1번의 "과제" 태그 글 -> 첫 번째 테스트 글 나옴
        # 6. borad_id=1, keyword=none, tags=["시험", "과제"] : 게시판 1번의 "시험" AND "과제" 태그 글 -> 첫 번째 테스트 글 나옴

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
    # -> 결과는 PostListItem 목록으로 반환
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