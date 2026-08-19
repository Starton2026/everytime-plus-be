# 담당: 서현 - 게시판
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from auth_utils import get_current_user_optional
from database import get_db
from models import Board, Post, User
from post_utils import paginate_posts
from schemas.board import BoardResponse
from schemas.common import Page
from schemas.post import PostListItem

router = APIRouter(prefix="/boards", tags=["boards"])

# 서버에 기본으로 존재해야 하는 게시판 3종
DEFAULT_BOARD_NAMES = ["자유 게시판", "새내기 게시판", "졸업생 게시판"]

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50


def ensure_default_boards(db: Session) -> None:
    """기본 게시판 3개가 없으면 생성한다.
    별도 시딩 스크립트 대신, 목록 조회 시마다 없는 것만 채워 넣는 방식(lazy)."""
    existing_names = {name for (name,) in db.query(Board.name).all()}
    for name in DEFAULT_BOARD_NAMES:
        if name not in existing_names:
            db.add(Board(name=name))
    db.commit()


@router.get("", response_model=list[BoardResponse])
def list_boards(db: Session = Depends(get_db)):
    """게시판 목록 조회. 로그인 불필요 (누구나 접근 가능)."""
    ensure_default_boards(db)
    return db.query(Board).order_by(Board.id).all()


@router.get("/{board_id}/posts", response_model=Page[PostListItem])
def list_posts_in_board(
    board_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    """특정 게시판의 게시글 목록 조회 (최신순, 페이지 단위). 로그인 불필요.
    검색/태그 필터가 걸린 조회는 준모의 /search 담당이라 여기선 다루지 않는다.

    응답 변환과 페이지 계산은 post_utils(재윤)에 모여 있어서 /search와 형태가 같다.
    """
    board = db.get(Board, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="게시판을 찾을 수 없습니다")

    query = (
        db.query(Post)
        .filter(Post.board_id == board_id)
        .order_by(Post.created_at.desc(), Post.id.desc())  # 최신 글이 위로
    )
    return paginate_posts(query, page, size, user)
