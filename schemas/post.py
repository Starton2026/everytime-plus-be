# 담당: 하은 - 게시글 CRUD 스키마
from pydantic import BaseModel, Field, field_validator

from schemas.common import UtcDateTime


class PostCreate(BaseModel):
    board_id: int
    title: str  # 1~100자, 공백만 입력 불가, 앞뒤 공백 자동 제거
    content: str  # 1~2000자
    tags: list[str] = Field(default_factory=list)  # 최대 3개
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
    """수정 요청. 검증 규칙은 작성과 동일하다. (is_anonymous는 수정할 수 없다)"""

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
    board_id: int
    title: str
    content_preview: str
    tags: list[str]
    like_count: int
    dislike_count: int
    comment_count: int  # 리스트 카드에 댓글 수를 표시하기 위함 (프론트 요청)
    author_nickname: str  # is_anonymous=True면 "익명"
    is_anonymous: bool
    created_at: UtcDateTime
    is_mine: bool  # 익명 글은 닉네임으로 작성자를 알 수 없어 서버가 판별해준다
    my_reaction: str | None  # "like" | "dislike" | None


class PostDetail(BaseModel):
    id: int
    board_id: int  # 상세 -> 목록 이동, 태그 클릭 시 어느 게시판으로 갈지 판단용
    title: str
    content: str
    tags: list[str]
    like_count: int
    dislike_count: int
    comment_count: int
    author_nickname: str
    is_anonymous: bool
    created_at: UtcDateTime
    is_mine: bool  # 수정/삭제 버튼 노출용
    my_reaction: str | None  # 내가 누른 좋아요/싫어요 (새로고침해도 상태 유지)
    # 댓글은 GET /posts/{id}/comments 로 따로 조회 (나희 담당과 겹치지 않게)
