# 테스트 데이터 시드 스크립트 (전원 공용)
# 사용법: python seed.py  (서버 실행 전/후 아무 때나, 여러 번 실행해도 안전)
# 기본 게시판 3개 + 테스트 유저 + 샘플 게시글을 만들어준다.
from auth_utils import hash_password
from database import Base, SessionLocal, engine
from models import Board, Post, Tag, User

Base.metadata.create_all(bind=engine)
db = SessionLocal()


def get_or_create(model, defaults=None, **kwargs):
    obj = db.query(model).filter_by(**kwargs).first()
    if obj is None:
        obj = model(**kwargs, **(defaults or {}))
        db.add(obj)
        db.commit()
        db.refresh(obj)
    return obj


boards = [get_or_create(Board, name=n) for n in ["자유 게시판", "새내기 게시판", "졸업생 게시판"]]

# 테스트 계정: 아이디 testuser / 비밀번호 test1234
tester = get_or_create(
    User, username="testuser",
    defaults={"nickname": "테스트유저", "hashed_password": hash_password("test1234")},
)

tag_exam = get_or_create(Tag, name="시험")
tag_hw = get_or_create(Tag, name="과제")

if not db.query(Post).filter_by(title="첫 번째 테스트 글").first():
    post = Post(
        board_id=boards[0].id,
        author_id=tester.id,
        title="첫 번째 테스트 글",
        content="시험 기간 과제 너무 많다... 댓글/좋아요 테스트용 글입니다.",
        is_anonymous=False,
    )
    post.tags = [tag_exam, tag_hw]
    db.add(post)
    db.commit()

print("시드 완료: 게시판 3개, 유저 testuser(pw: test1234), 샘플 게시글 1개")
db.close()
