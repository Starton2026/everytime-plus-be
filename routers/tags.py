# 담당: 재윤 - 태그 목록
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Tag

router = APIRouter(prefix="/tags", tags=["tags"])

# 태그 선택 UI에 항상 노출할 기본 태그 (기획서 태그 목록).
# 게시글 작성 시 태그는 자유 입력이라, DB에 있는 것만 내려주면 새 DB에서 선택지가
# 비어버린다. 그래서 기본 목록을 고정으로 두고 실제 사용된 태그를 뒤에 덧붙인다.
DEFAULT_TAGS = [
    "질문", "정보", "잡담", "고민", "추천",
    "후기", "맛집", "연애", "축제",
    "수강신청", "수업", "시간표", "과제", "시험",
    "동아리", "기숙사",
    "취업", "이직", "면접", "진로", "자격증", "대학원", "커리어",
]


@router.get("", response_model=list[str])
def list_tags(db: Session = Depends(get_db)):
    """태그 목록 조회. 로그인 불필요.

    기본 태그 + 사용자가 글을 쓰면서 새로 만든 태그를 합쳐서 내려준다.
    """
    used_names = [name for (name,) in db.query(Tag.name).order_by(Tag.name).all()]
    extra_names = [name for name in used_names if name not in DEFAULT_TAGS]

    return DEFAULT_TAGS + extra_names
