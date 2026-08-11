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
