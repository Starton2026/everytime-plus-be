# 담당: 나희 - 좋아요/싫어요 (게시글 + 댓글)
# 규칙: 사용자당 1회, like/dislike 중 하나만.
#  - 같은 걸 다시 누르면 취소
#  - 다른 걸 누르면 교체
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from database import get_db
from models import Comment, CommentReaction, Post, PostReaction, User
from schemas.reaction import ReactionRequest, ReactionResponse

router = APIRouter(tags=["reactions"])


def apply_reaction(existing, new_type: str, db: Session, create_new) -> None:
    """생성/교체/취소 공통 로직. existing이 없으면 create_new()로 생성."""
    if existing is None:
        db.add(create_new())
    elif existing.type == new_type:
        db.delete(existing)  # 같은 버튼 다시 누름 → 취소
    else:
        existing.type = new_type  # 다른 버튼 누름 → 교체
    db.commit()


def count_response(reactions, user_id: int) -> ReactionResponse:
    return ReactionResponse(
        like_count=sum(1 for r in reactions if r.type == "like"),
        dislike_count=sum(1 for r in reactions if r.type == "dislike"),
        my_reaction=next((r.type for r in reactions if r.user_id == user_id), None),
    )


@router.post("/posts/{post_id}/reaction", response_model=ReactionResponse)
def react_to_post(
    post_id: int,
    body: ReactionRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")

    existing = (
        db.query(PostReaction)
        .filter(PostReaction.post_id == post_id, PostReaction.user_id == user.id)
        .first()
    )
    apply_reaction(
        existing, body.type, db,
        lambda: PostReaction(post_id=post_id, user_id=user.id, type=body.type),
    )
    db.refresh(post)
    return count_response(post.reactions, user.id)


@router.post("/comments/{comment_id}/reaction", response_model=ReactionResponse)
def react_to_comment(
    comment_id: int,
    body: ReactionRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    comment = db.get(Comment, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다")

    existing = (
        db.query(CommentReaction)
        .filter(CommentReaction.comment_id == comment_id, CommentReaction.user_id == user.id)
        .first()
    )
    apply_reaction(
        existing, body.type, db,
        lambda: CommentReaction(comment_id=comment_id, user_id=user.id, type=body.type),
    )
    db.refresh(comment)
    return count_response(comment.reactions, user.id)
