# 공통 파일 - 담당: 재윤 / 사용: 서현·하은·준모
# 게시글 응답 변환과 페이지네이션.
#
# 목록(서현) / 검색(준모) / 상세(하은)가 같은 형태를 내려주도록 여기 한 곳에서 만든다.
# 예전에는 boards.py와 search.py가 각자 PostListItem을 조립해서 미리보기 길이가
# 서로 달랐고, is_mine 같은 필드를 한쪽에만 추가하기 쉬웠다.
#
# 사용 예:
#   from post_utils import paginate_posts, to_post_detail
#
#   query = db.query(Post).filter(...).order_by(Post.created_at.desc())
#   return paginate_posts(query, page, size, user)
from math import ceil

from sqlalchemy.orm import Query

from models import Post, User

# 게시글 리스트에서 본문을 미리보기로 자를 글자 수 (디자인상 카드에 2줄 정도만 노출)
CONTENT_PREVIEW_LENGTH = 60

ANONYMOUS_NICKNAME = "익명"


def build_preview(content: str) -> str:
    """본문이 길면 미리보기 글자 수까지만 자르고 "..." 을 붙인다."""
    if len(content) <= CONTENT_PREVIEW_LENGTH:
        return content
    return content[:CONTENT_PREVIEW_LENGTH] + "..."


def author_nickname(post: Post) -> str:
    return ANONYMOUS_NICKNAME if post.is_anonymous else post.author.nickname


def count_reactions(post: Post, reaction_type: str) -> int:
    return sum(1 for reaction in post.reactions if reaction.type == reaction_type)


def find_my_reaction(post: Post, user: User | None) -> str | None:
    """로그인한 사용자가 이 글에 누른 반응. 없으면 None.

    프론트가 새로고침 후에도 좋아요/싫어요 눌린 상태를 유지하려면 조회 응답에
    이 값이 있어야 한다.
    """
    if user is None:
        return None
    return next((r.type for r in post.reactions if r.user_id == user.id), None)


def is_mine(post: Post, user: User | None) -> bool:
    """작성자 본인 여부.

    익명 글은 author_nickname이 "익명"으로 나가서 프론트가 닉네임 비교로는
    작성자를 알 수 없다. 수정/삭제 버튼 노출을 위해 서버가 판별해준다.
    """
    return user is not None and post.author_id == user.id


def to_post_list_item(post: Post, user: User | None) -> dict:
    """Post ORM 객체를 목록 응답용(PostListItem) 형태로 변환한다."""
    return {
        "id": post.id,
        "board_id": post.board_id,
        "title": post.title,
        "content_preview": build_preview(post.content),
        "tags": [tag.name for tag in post.tags],  # Tag 객체 리스트 -> 이름 문자열 리스트
        "like_count": count_reactions(post, "like"),
        "dislike_count": count_reactions(post, "dislike"),
        "comment_count": len(post.comments),
        "author_nickname": author_nickname(post),
        "is_anonymous": post.is_anonymous,
        "created_at": post.created_at,
        "is_mine": is_mine(post, user),
        "my_reaction": find_my_reaction(post, user),
    }


def to_post_detail(post: Post, user: User | None) -> dict:
    """Post ORM 객체를 상세 응답용(PostDetail) 형태로 변환한다."""
    return {
        "id": post.id,
        "board_id": post.board_id,
        "title": post.title,
        "content": post.content,
        "tags": [tag.name for tag in post.tags],
        "like_count": count_reactions(post, "like"),
        "dislike_count": count_reactions(post, "dislike"),
        "comment_count": len(post.comments),
        "author_nickname": author_nickname(post),
        "is_anonymous": post.is_anonymous,
        "created_at": post.created_at,
        "is_mine": is_mine(post, user),
        "my_reaction": find_my_reaction(post, user),
    }


def paginate_posts(query: Query, page: int, size: int, user: User | None) -> dict:
    """정렬까지 끝난 게시글 쿼리를 페이지 단위로 잘라 Page 형태로 만든다.

    page는 1부터 시작한다. 범위를 벗어나면 마지막 페이지로 맞춰준다.
    """
    total_elements = query.count()
    total_pages = max(1, ceil(total_elements / size))
    safe_page = min(max(page, 1), total_pages)

    posts = query.offset((safe_page - 1) * size).limit(size).all()

    return {
        "items": [to_post_list_item(post, user) for post in posts],
        "page": safe_page,
        "size": size,
        "total_pages": total_pages,
        "total_elements": total_elements,
    }
