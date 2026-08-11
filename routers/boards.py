# 담당: 서현 - 게시판
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(prefix="/boards", tags=["boards"])


@router.get("")
def list_boards(db: Session = Depends(get_db)):
    # TODO(서현): 게시판 목록 (자유/새내기/졸업생)
    #  기본 게시판 3개는 서버 최초 실행 시 없으면 생성하는 방식 추천
    raise NotImplementedError


@router.get("/{board_id}/posts")
def list_posts_in_board(board_id: int, db: Session = Depends(get_db)):
    # TODO(서현): 해당 게시판의 게시글 리스트 (PostListItem 목록)
    #  검색/태그 필터가 걸린 조회는 준모의 /search 담당
    raise NotImplementedError
