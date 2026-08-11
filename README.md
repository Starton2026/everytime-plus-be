# everytime-plus-be

에브리타임 클론 백엔드 (FastAPI + SQLite). 태그 기반 게시글 필터링이 핵심 기능인 게시판 서비스입니다.
프론트엔드는 React로 별도 저장소에서 개발하고, 이 서버의 REST API를 호출합니다.

## 실행 방법

```bash
# 1. 가상환경 생성 + 활성화 (최초 1회)
python3 -m venv .venv
source .venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 서버 실행 (everytime.db 파일이 자동 생성됨)
uvicorn main:app --reload
```

- API 문서(Swagger): http://localhost:8000/docs — 브라우저에서 바로 API 테스트 가능
- DB: SQLite 파일 하나(`everytime.db`)로 동작. 별도 설치 불필요. 꼬이면 파일 지우고 서버 재시작하면 초기화됨

## 역할 분담

| 담당 | 기능 | 파일 |
|------|------|------|
| 나희 | 로그인/회원가입, 댓글, 좋아요/싫어요 | `routers/auth.py`, `routers/comments.py`, `routers/reactions.py` + `schemas/auth.py`, `schemas/comment.py`, `schemas/reaction.py` + `auth_utils.py` |
| 서현 | 게시판 (목록/게시판별 글 리스트) | `routers/boards.py` + `schemas/board.py` |
| 하은 | 게시글 CRUD | `routers/posts.py` + `schemas/post.py` |
| 준모 | 검색 + 태그 필터링 | `routers/search.py` + `schemas/search.py` |

## 폴더 구조

```
everytime-plus-be/
├── main.py              # 앱 진입점. 라우터 등록 + CORS 완료 → 수정 금지
├── database.py          # SQLite 연결/세션 → 수정 금지
├── models.py            # 테이블 정의 (User, Board, Post, Tag, Comment, Reaction) → 변경은 팀 합의 후
├── auth_utils.py        # JWT + 비밀번호 해싱 + get_current_user (나희 작성, 전원 사용)
├── requirements.txt
├── schemas/             # 요청/응답 Pydantic 스키마 (담당자별 파일)
│   ├── auth.py  comment.py  reaction.py    # 나희
│   ├── board.py                            # 서현
│   ├── post.py                             # 하은
│   └── search.py                           # 준모
└── routers/             # API 엔드포인트 (담당자별 파일, TODO 스텁 상태)
    ├── auth.py  comments.py  reactions.py  # 나희
    ├── boards.py                           # 서현
    ├── posts.py                            # 하은
    └── search.py                           # 준모
```

## 협업 규칙

- **자기 담당 파일만 수정**합니다. 공통 파일(`main.py`, `database.py`, `models.py`)은 이미 완성되어 있어 건드릴 일이 없고, 바꿔야 하면 팀 합의 후 수정합니다.
- 각 라우터 파일 안에 구현할 내용이 `TODO(이름)` 주석으로 정리되어 있습니다.
- 로그인이 필요한 API는 파라미터에 `user: User = Depends(get_current_user)`만 추가하면 됩니다 (`auth_utils.py` 상단 주석 참고).

## API 개요

| 메서드 | 경로 | 설명 | 담당 |
|--------|------|------|------|
| POST | `/auth/signup` | 회원가입 (성공 시 토큰 발급 = 자동 로그인) | 나희 |
| POST | `/auth/login` | 로그인 | 나희 |
| GET | `/auth/me` | 내 정보 조회 (토큰 필요) | 나희 |
| GET | `/boards` | 게시판 목록 | 서현 |
| GET | `/boards/{id}/posts` | 게시판별 게시글 리스트 | 서현 |
| POST | `/posts` | 게시글 작성 (태그 최대 3개, 익명 선택) | 하은 |
| GET | `/posts/{id}` | 게시글 상세 | 하은 |
| PUT / DELETE | `/posts/{id}` | 게시글 수정/삭제 (작성자만) | 하은 |
| GET | `/search?board_id=&keyword=&tags=` | 검색 + 태그 필터 (AND 조건) | 준모 |
| GET / POST | `/posts/{id}/comments` | 댓글 목록/작성 | 나희 |
| DELETE | `/posts/{id}/comments/{cid}` | 댓글 삭제 (작성자만) | 나희 |
| POST | `/posts/{id}/reaction` | 게시글 좋아요/싫어요 | 나희 |
| POST | `/comments/{id}/reaction` | 댓글 좋아요/싫어요 | 나희 |

## DB 구조 (models.py)

- **users** — username(아이디), nickname, hashed_password
- **boards** — 자유/새내기/졸업생 게시판
- **posts** — 제목, 본문, 익명 여부, 작성자·게시판 FK
- **tags** + **post_tags** — 태그, 게시글과 다대다 연결 (게시글당 최대 3개는 API에서 검증)
- **comments** — 내용, 익명 여부, 게시글·작성자 FK
- **post_reactions / comment_reactions** — like/dislike, (사용자, 대상) 조합당 1개 제약
