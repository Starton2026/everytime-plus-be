# 담당: 하은 - 게시글 CRUD
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth_utils import get_current_user, get_current_user_optional
from database import get_db
from models import Board, Post, Tag, User
from post_utils import to_post_detail
from schemas.post import PostCreate, PostDetail, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


def get_post_or_404(post_id: int, db: Session) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    return post


def attach_tags(post: Post, tag_names: list[str], db: Session) -> None:
    """태그 이름으로 Tag를 찾고, 없으면 만들어서 게시글에 연결한다."""
    post.tags.clear()

    for tag_name in tag_names:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()

        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()

        post.tags.append(tag)


@router.post("", response_model=PostDetail)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    board = db.query(Board).filter(Board.id == data.board_id).first()

    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시판을 찾을 수 없습니다.",
        )

    new_post = Post(
        board_id=data.board_id,
        author_id=user.id,
        title=data.title,
        content=data.content,
        is_anonymous=data.is_anonymous,
    )
    attach_tags(new_post, data.tags, db)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return to_post_detail(new_post, user)


@router.get("/{post_id}", response_model=PostDetail)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    """게시글 상세 조회. 로그인 불필요.

    로그인 상태면 is_mine / my_reaction이 함께 내려간다.
    (프론트에서 수정·삭제 버튼 노출, 좋아요 눌린 상태 유지에 쓴다)
    """
    post = get_post_or_404(post_id, db)
    return to_post_detail(post, user)


@router.put("/{post_id}", response_model=PostDetail)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = get_post_or_404(post_id, db)

    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="게시글을 수정할 권한이 없습니다.",
        )

    post.title = data.title
    post.content = data.content
    attach_tags(post, data.tags, db)

    db.commit()
    db.refresh(post)

    return to_post_detail(post, user)


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = get_post_or_404(post_id, db)

    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="게시글을 삭제할 권한이 없습니다.",
        )

    db.delete(post)
    db.commit()

    return {"message": "게시글이 삭제되었습니다."}
