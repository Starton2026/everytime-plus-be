# 공통 파일 - 프로젝트 시작 시 다같이 확정한 테이블 정의.
# 이후 변경이 필요하면 반드시 팀 합의 후 수정할 것 (전원 코드에 영향)
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from database import Base


def utcnow() -> datetime:
    """생성 시각 기본값. 타임존 없는 UTC로 통일해서 저장한다.

    datetime.utcnow()는 Python 3.12에서 deprecated 되어 같은 값을 주는 방식으로 바꿨다.
    응답으로 나갈 때 UTC임을 표시하는 건 schemas/common.py의 UtcDateTime이 맡는다.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)

# 게시글 <-> 태그 다대다 연결 테이블 (게시글당 태그 최대 3개는 API에서 검증)
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)  # 아이디 (4~20자, 영문+숫자)
    nickname = Column(String(10), unique=True, nullable=False)  # 닉네임 (10자 이하)
    hashed_password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)  # 자유/새내기/졸업생

    posts = relationship("Post", back_populates="board")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    board_id = Column(ForeignKey("boards.id"), nullable=False)
    author_id = Column(ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)  # 1~100자
    content = Column(Text, nullable=False)  # 1~2000자
    is_anonymous = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    board = relationship("Board", back_populates="posts")
    author = relationship("User", back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    reactions = relationship("PostReaction", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(ForeignKey("posts.id"), nullable=False)
    author_id = Column(ForeignKey("users.id"), nullable=False)
    content = Column(String(300), nullable=False)  # 1~300자
    is_anonymous = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    reactions = relationship("CommentReaction", back_populates="comment", cascade="all, delete-orphan")


class PostReaction(Base):
    """게시글 좋아요/싫어요. 사용자당 게시글 하나에 1개만 (like 또는 dislike)."""

    __tablename__ = "post_reactions"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    post_id = Column(ForeignKey("posts.id"), nullable=False)
    type = Column(String(10), nullable=False)  # "like" | "dislike"

    post = relationship("Post", back_populates="reactions")


class CommentReaction(Base):
    """댓글 좋아요/싫어요. 규칙은 게시글과 동일."""

    __tablename__ = "comment_reactions"
    __table_args__ = (UniqueConstraint("user_id", "comment_id"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    comment_id = Column(ForeignKey("comments.id"), nullable=False)
    type = Column(String(10), nullable=False)  # "like" | "dislike"

    comment = relationship("Comment", back_populates="reactions")
