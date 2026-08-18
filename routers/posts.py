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
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class PostCreate(BaseModel):
    board_id: int
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    is_anonymous: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("제목을 입력해주세요.")

        if len(value) > 100:
            raise ValueError("제목은 100자 이하로 입력해주세요.")

        return value

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("내용을 입력해주세요.")

        if len(value) > 2000:
            raise ValueError("내용은 2000자 이하로 입력해주세요.")

        return value

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        if len(value) > 3:
            raise ValueError("태그는 최대 3개까지 입력할 수 있습니다.")

        cleaned_tags = []

        for tag in value:
            tag = tag.strip()

            if not tag:
                raise ValueError("빈 태그는 입력할 수 없습니다.")

            if len(tag) > 20:
                raise ValueError("태그는 20자 이하로 입력해주세요.")

            cleaned_tags.append(tag)

        if len(cleaned_tags) != len(set(cleaned_tags)):
            raise ValueError("같은 태그를 중복해서 입력할 수 없습니다.")

        return cleaned_tags


class PostUpdate(BaseModel):
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("제목을 입력해주세요.")

        if len(value) > 100:
            raise ValueError("제목은 100자 이하로 입력해주세요.")

        return value

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("내용을 입력해주세요.")

        if len(value) > 2000:
            raise ValueError("내용은 2000자 이하로 입력해주세요.")

        return value

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        if len(value) > 3:
            raise ValueError("태그는 최대 3개까지 입력할 수 있습니다.")

        cleaned_tags = []

        for tag in value:
            tag = tag.strip()

            if not tag:
                raise ValueError("빈 태그는 입력할 수 없습니다.")

            if len(tag) > 20:
                raise ValueError("태그는 20자 이하로 입력해주세요.")

            cleaned_tags.append(tag)

        if len(cleaned_tags) != len(set(cleaned_tags)):
            raise ValueError("같은 태그를 중복해서 입력할 수 없습니다.")

        return cleaned_tags


class PostListItem(BaseModel):
    """게시글 리스트용: 본문은 일부만"""

    id: int
    title: str
    content_preview: str
    tags: list[str]
    like_count: int
    dislike_count: int
    author_nickname: str
    created_at: datetime


class PostDetail(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]
    like_count: int
    dislike_count: int
    author_nickname: str
    is_anonymous: bool
    created_at: datetime