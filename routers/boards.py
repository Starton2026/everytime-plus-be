# 담당: 서현 - 게시판
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Board, Post
from schemas.board import BoardResponse
from schemas.post import PostListItem

router = APIRouter(prefix="/boards", tags=["boards"])

# 서버에 기본으로 존재해야 하는 게시판 3종
DEFAULT_BOARD_NAMES = ["자유 게시판", "새내기 게시판", "졸업생 게시판"]
# 게시글 리스트에서 본문을 미리보기로 자를 글자 수 (디자인상 카드에 2줄 정도만 노출)
CONTENT_PREVIEW_LENGTH = 60


def ensure_default_boards(db: Session) -> None:
    """기본 게시판 3개가 없으면 생성한다.
    별도 시딩 스크립트 대신, 목록 조회 시마다 없는 것만 채워 넣는 방식(lazy)."""
    existing_names = {name for (name,) in db.query(Board.name).all()}
    for name in DEFAULT_BOARD_NAMES:
        if name not in existing_names:
            db.add(Board(name=name))
    db.commit()


def to_post_list_item(post: Post) -> PostListItem:
    """Post ORM 객체를 목록 응답용 스키마(PostListItem)로 변환한다."""
    # 본문이 길면 미리보기 글자 수까지만 자르고 "..." 표시
    content_preview = post.content[:CONTENT_PREVIEW_LENGTH]
    if len(post.content) > CONTENT_PREVIEW_LENGTH:
        content_preview += "..."
    return PostListItem(
        id=post.id,
        title=post.title,
        content_preview=content_preview,
        tags=[tag.name for tag in post.tags],  # Tag 객체 리스트 -> 이름 문자열 리스트
        like_count=sum(1 for r in post.reactions if r.type == "like"),
        dislike_count=sum(1 for r in post.reactions if r.type == "dislike"),
        author_nickname="익명" if post.is_anonymous else post.author.nickname,
        created_at=post.created_at,
    )


@router.get("", response_model=list[BoardResponse])
def list_boards(db: Session = Depends(get_db)):
    """게시판 목록 조회. 로그인 불필요 (누구나 접근 가능)."""
    ensure_default_boards(db)
    return db.query(Board).order_by(Board.id).all()


@router.get("/{board_id}/posts", response_model=list[PostListItem])
def list_posts_in_board(board_id: int, db: Session = Depends(get_db)):
    """특정 게시판의 게시글 목록 조회 (최신순). 로그인 불필요.
    검색/태그 필터가 걸린 조회는 준모의 /search 담당이라 여기선 다루지 않는다."""
    board = db.get(Board, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="게시판을 찾을 수 없습니다")

    posts = (
        db.query(Post)
        .filter(Post.board_id == board_id)
        .order_by(Post.created_at.desc())  # 최신 글이 위로
        .all()
    )
    return [to_post_list_item(post) for post in posts]
