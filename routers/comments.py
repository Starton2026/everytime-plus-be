# 담당: 나희 - 댓글 (작성 / 목록 / 삭제. 수정은 스펙상 불가)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth_utils import get_current_user, get_current_user_optional
from database import get_db
from models import Comment, Post, User
from schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])


def get_post_or_404(post_id: int, db: Session) -> Post:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
    return post


def to_comment_response(comment: Comment, user: User | None) -> CommentResponse:
    my_reaction = None
    if user is not None:
        my_reaction = next(
            (r.type for r in comment.reactions if r.user_id == user.id), None
        )
    return CommentResponse(
        id=comment.id,
        content=comment.content,
        is_anonymous=comment.is_anonymous,
        author_nickname="익명" if comment.is_anonymous else comment.author.nickname,
        like_count=sum(1 for r in comment.reactions if r.type == "like"),
        dislike_count=sum(1 for r in comment.reactions if r.type == "dislike"),
        created_at=comment.created_at,
        is_mine=user is not None and comment.author_id == user.id,
        my_reaction=my_reaction,
    )


@router.get("", response_model=list[CommentResponse])
def list_comments(
    post_id: int,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    post = get_post_or_404(post_id, db)
    return [to_comment_response(c, user) for c in post.comments]


@router.post("", response_model=CommentResponse)
def create_comment(
    post_id: int,
    body: CommentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    get_post_or_404(post_id, db)
    comment = Comment(
        post_id=post_id,
        author_id=user.id,
        content=body.content,
        is_anonymous=body.is_anonymous,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return to_comment_response(comment, user)


@router.delete("/{comment_id}", status_code=204)
def delete_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    comment = db.get(Comment, comment_id)
    if comment is None or comment.post_id != post_id:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다")
    if comment.author_id != user.id:
        raise HTTPException(status_code=403, detail="본인의 댓글만 삭제할 수 있습니다")
    db.delete(comment)
    db.commit()
