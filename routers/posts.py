# 담당: 하은 - 게시글 CRUD
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from database import get_db
from models import User

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("")
def create_post(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # TODO(하은): 게시글 작성 (PostCreate)
    #  - 제목 1~100자(trim), 본문 1~2000자, 태그 최대 3개
    #  - 태그는 이름으로 받아서 Tag 테이블에 없으면 생성 후 연결
    raise NotImplementedError


@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    # TODO(하은): 게시글 상세 (PostDetail)
    #  - like/dislike 카운트는 reactions 관계에서 집계
    #  - is_anonymous면 author_nickname을 "익명"으로
    raise NotImplementedError


@router.put("/{post_id}")
def update_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # TODO(하은): 게시글 수정 (PostUpdate). 작성자 본인만 (아니면 403)
    raise NotImplementedError


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # TODO(하은): 게시글 삭제. 작성자 본인만 (아니면 403)
    raise NotImplementedError


#---------------------------------------------------------------

# 담당: 하은 - 게시글 CRUD 스키마
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from database import get_db
from models import User, Post, Tag, Board
from schemas.post import PostCreate, PostUpdate, PostDetail

router = APIRouter(prefix="/posts", tags=["posts"])


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

    for tag_name in data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()

        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()

        new_post.tags.append(tag)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "id": new_post.id,
        "title": new_post.title,
        "content": new_post.content,
        "tags": [tag.name for tag in new_post.tags],
        "like_count": 0,
        "dislike_count": 0,
        "author_nickname": "익명" if new_post.is_anonymous else user.nickname,
        "is_anonymous": new_post.is_anonymous,
        "created_at": new_post.created_at,
    }


@router.get("/{post_id}", response_model=PostDetail)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    like_count = 0
    dislike_count = 0

    for reaction in post.reactions:
        if reaction.type == "like":
            like_count += 1
        elif reaction.type == "dislike":
            dislike_count += 1

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "tags": [tag.name for tag in post.tags],
        "like_count": like_count,
        "dislike_count": dislike_count,
        "author_nickname": "익명" if post.is_anonymous else post.author.nickname,
        "is_anonymous": post.is_anonymous,
        "created_at": post.created_at,
    }


@router.put("/{post_id}", response_model=PostDetail)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="게시글을 수정할 권한이 없습니다.",
        )

    post.title = data.title
    post.content = data.content
    post.tags.clear()

    for tag_name in data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()

        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()

        post.tags.append(tag)

    db.commit()
    db.refresh(post)

    like_count = 0
    dislike_count = 0

    for reaction in post.reactions:
        if reaction.type == "like":
            like_count += 1
        elif reaction.type == "dislike":
            dislike_count += 1

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "tags": [tag.name for tag in post.tags],
        "like_count": like_count,
        "dislike_count": dislike_count,
        "author_nickname": "익명" if post.is_anonymous else post.author.nickname,
        "is_anonymous": post.is_anonymous,
        "created_at": post.created_at,
    }


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="게시글을 삭제할 권한이 없습니다.",
        )

    db.delete(post)
    db.commit()

    return {"message": "게시글이 삭제되었습니다."}