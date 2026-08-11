# 담당: 나희 - 댓글 (작성 / 목록 / 삭제. 수정은 스펙상 불가)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from database import get_db
from models import User

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])


@router.get("")
def list_comments(post_id: int, db: Session = Depends(get_db)):
    # TODO(나희): 댓글 목록. is_anonymous면 author_nickname을 "익명"으로
    raise NotImplementedError


@router.post("")
def create_comment(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # TODO(나희): 댓글 작성 (CommentCreate, 1~300자)
    raise NotImplementedError


@router.delete("/{comment_id}")
def delete_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # TODO(나희): 작성자 본인만 삭제 가능 (아니면 403)
    raise NotImplementedError
