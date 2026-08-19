# 담당: 하은 - 게시글 CRUD 스키마
from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str  # 1~100자, 공백만 입력 불가, 앞뒤 공백 자동 제거
    content: str  # 1~2000자
    tags: list[str] = []  # 최대 3개
    is_anonymous: bool = False
    # TODO(하은): field_validator로 유효성 규칙 구현


class PostUpdate(BaseModel):
    title: str
    content: str
    tags: list[str] = []


class PostListItem(BaseModel):
    """게시글 리스트용: 본문은 일부만"""

    id: int
    title: str
    content_preview: str
    tags: list[str]
    like_count: int
    dislike_count: int
    author_nickname: str  # is_anonymous=True면 "익명"
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
    # 댓글은 GET /posts/{id}/comments 로 따로 조회 (나희 담당과 겹치지 않게)

#--------------------------------------------------------------------------

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