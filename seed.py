# 테스트 데이터 시드 스크립트 (전원 공용)
# 사용법: python seed.py  (서버 실행 전/후 아무 때나, 여러 번 실행해도 안전)
# 기본 게시판 3개 + 테스트 유저 + 샘플 게시글을 만들어준다.
#
# main.py가 서버 기동 시에도 seed()를 호출한다.
# Render 무료 플랜은 디스크가 유지되지 않아 서버가 깨어날 때마다 everytime.db가
# 빈 파일로 다시 만들어지는데, 그대로 두면 게시판·계정·게시글이 전부 사라져서
# 로그인 정보가 없는 환경(시크릿 모드 등)에서는 아무것도 할 수 없다.
from sqlalchemy.orm import Session

from auth_utils import hash_password
from database import Base, SessionLocal, engine
from models import Board, Post, Tag, User

BOARD_NAMES = ["자유 게시판", "새내기 게시판", "졸업생 게시판"]

# 테스트 계정: 아이디 testuser / 비밀번호 test1234
TEST_USERNAME = "testuser"
TEST_NICKNAME = "테스트유저"
TEST_PASSWORD = "test1234"

# 태그 필터를 바로 확인할 수 있도록 게시판·태그를 섞어서 넣는다.
# (board = BOARD_NAMES 인덱스, tags = 태그 이름)
SAMPLE_POSTS = [
    {
        "board": 0,
        "title": "첫 번째 테스트 글",
        "content": "시험 기간 과제 너무 많다... 댓글/좋아요 테스트용 글입니다.",
        "tags": ["시험", "과제"],
        "is_anonymous": False,
    },
    {
        "board": 0,
        "title": "중간고사 시험범위 아는 사람?",
        "content": "자료구조 중간고사 범위가 어디까지인지 공지에 없는데 아시는 분 있나요?",
        "tags": ["시험", "질문"],
        "is_anonymous": True,
    },
    {
        "board": 0,
        "title": "학식 신메뉴 후기",
        "content": "학생회관 2층에 새로 나온 메뉴 먹어봤습니다. 가격 대비 양이 넉넉해요.",
        "tags": ["맛집", "후기"],
        "is_anonymous": False,
    },
    {
        "board": 1,
        "title": "새내기인데 수강신청 어떻게 하나요",
        "content": "다음 주가 수강신청인데 장바구니를 미리 담아두는 건지 궁금합니다.",
        "tags": ["수강신청", "질문"],
        "is_anonymous": True,
    },
    {
        "board": 1,
        "title": "1학년 시간표 짜는 팁",
        "content": "공강 하루 만들려고 무리하게 몰면 체력이 안 됩니다. 1교시는 두 개까지만.",
        "tags": ["시간표", "정보"],
        "is_anonymous": False,
    },
    {
        "board": 2,
        "title": "신입 면접에서 자주 나온 질문 모음",
        "content": "프로젝트에서 가장 어려웠던 문제와 해결 과정을 제일 많이 물어봅니다.",
        "tags": ["면접", "취업", "정보"],
        "is_anonymous": False,
    },
    {
        "board": 2,
        "title": "대학원 진학 고민 중입니다",
        "content": "취업이랑 대학원 사이에서 계속 고민하고 있어요. 다녀오신 분들 만족하시나요?",
        "tags": ["대학원", "진로", "고민"],
        "is_anonymous": True,
    },
]


def get_or_create(db: Session, model, defaults=None, **kwargs):
    obj = db.query(model).filter_by(**kwargs).first()
    if obj is None:
        obj = model(**kwargs, **(defaults or {}))
        db.add(obj)
        db.commit()
        db.refresh(obj)
    return obj


def seed(verbose: bool = True) -> None:
    """기본 게시판 · 테스트 계정 · 샘플 게시글을 채운다. 이미 있으면 건드리지 않는다."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        boards = [get_or_create(db, Board, name=name) for name in BOARD_NAMES]

        tester = get_or_create(
            db,
            User,
            username=TEST_USERNAME,
            defaults={
                "nickname": TEST_NICKNAME,
                "hashed_password": hash_password(TEST_PASSWORD),
            },
        )

        created = 0
        for sample in SAMPLE_POSTS:
            if db.query(Post).filter_by(title=sample["title"]).first():
                continue

            post = Post(
                board_id=boards[sample["board"]].id,
                author_id=tester.id,
                title=sample["title"],
                content=sample["content"],
                is_anonymous=sample["is_anonymous"],
            )
            post.tags = [get_or_create(db, Tag, name=name) for name in sample["tags"]]
            db.add(post)
            created += 1

        db.commit()

        if verbose:
            print(
                f"시드 완료: 게시판 {len(boards)}개, "
                f"유저 {TEST_USERNAME}(pw: {TEST_PASSWORD}), 게시글 {created}개 추가"
            )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
