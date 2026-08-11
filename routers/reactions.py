# 담당: 나희 - 좋아요/싫어요 (게시글 + 댓글)
# 규칙: 사용자당 1회, like/dislike 중 하나만. 같은 걸 다시 누르면 취소,
#       다른 걸 누르면 교체 (프론트와 합의된 동작으로 구현)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from database import get_db
from models import User

router = APIRouter(tags=["reactions"])


@router.post("/posts/{post_id}/reaction")
def react_to_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # TODO(나희): ReactionRequest 받아 PostReaction 생성/교체/취소
    #  후 ReactionResponse(카운트 + 내 상태) 반환
    raise NotImplementedError


@router.post("/comments/{comment_id}/reaction")
def react_to_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # TODO(나희): 게시글과 동일한 로직으로 CommentReaction 처리
    raise NotImplementedError
