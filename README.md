# everytime-plus-be

에브리타임 클론 백엔드 (FastAPI + SQLite). 태그 기반 게시글 필터링이 핵심 기능인 게시판 서비스입니다.
프론트엔드는 React로 별도 저장소에서 개발하고, 이 서버의 REST API를 호출합니다.

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 팀명 | **스타톤 3팀** |
| 팀원 | 나희 · 서현 · 하은 · 준모 · 재윤 (역할 분담은 아래 참고) |
| 고른 서비스 | **에브리타임** (대학 커뮤니티 앱) |
| 개선한 점 | **게시글에 태그 기능 추가** |
| 이 저장소 | 백엔드 (FastAPI + SQLite) — 프론트엔드는 [everytime-plus-fe](https://github.com/Starton2026/everytime-plus-fe) |

### 무엇을 왜 개선했나

원래 에브리타임에서 글을 분류하는 수단은 게시판뿐입니다. 특정 주제의 글을 찾으려면 목록을 계속
넘겨보거나 검색어가 정확히 맞아떨어지기를 기대해야 합니다.

여기에 **태그**를 더했습니다. 글에 태그를 최대 3개까지 붙일 수 있고, 태그로 게시글을 걸러 볼 수
있습니다. 여러 태그를 고르면 그것을 **모두** 가진 글만 남고(AND 조건), 검색어와도 함께 걸립니다.

서버에서는 `tags` + `post_tags` 테이블로 게시글과 태그를 다대다로 연결하고,
`GET /search`가 검색어와 태그 조건을 함께 처리합니다. (담당: 준모)

## 실행 방법

```bash
# 1. 가상환경 생성 + 활성화 (최초 1회)
python3 -m venv .venv
source .venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 테스트 데이터 생성 (게시판 3개 + 테스트 유저 + 샘플 게시글, 여러 번 실행해도 안전)
python seed.py

# 4. 서버 실행 (everytime.db 파일이 자동 생성됨)
uvicorn main:app --reload
```

- API 문서(Swagger): http://localhost:8000/docs — 브라우저에서 바로 API 테스트 가능
- DB: SQLite 파일 하나(`everytime.db`)로 동작. 별도 설치 불필요. 꼬이면 파일 지우고 서버 재시작하면 초기화됨

## 역할 분담

| 담당 | 기능 | 파일 | 상태 |
|------|------|------|------|
| 나희 | 로그인/회원가입, 댓글, 좋아요/싫어요 | `routers/auth.py`, `routers/comments.py`, `routers/reactions.py` + `schemas/auth.py`, `schemas/comment.py`, `schemas/reaction.py` + `auth_utils.py` | ✅ 완료 |
| 서현 | 게시판 (목록/게시판별 글 리스트) | `routers/boards.py` + `schemas/board.py` | ✅ 완료 |
| 하은 | 게시글 CRUD | `routers/posts.py` + `schemas/post.py` | ✅ 완료 |
| 준모 | 검색 + 태그 필터링 | `routers/search.py` + `schemas/search.py` | ✅ 완료 |
| 재윤 | 태그 목록, 목록 응답/페이지네이션 공통화 | `routers/tags.py` + `schemas/common.py` + `post_utils.py` | ✅ 완료 |

인증이 필요한 API를 만들 때는 `auth_utils.py`의 `get_current_user`를 쓰면 되고,
비로그인도 접근 가능하지만 로그인 시 "내 상태"(is_mine 등)를 함께 주고 싶으면 `get_current_user_optional`을 쓰면 됩니다.
사용 예시는 `routers/comments.py` 참고.

## 폴더 구조

```
everytime-plus-be/
├── main.py              # 앱 진입점. 라우터 등록 + CORS 완료 → 수정 금지
├── database.py          # SQLite 연결/세션 → 수정 금지
├── models.py            # 테이블 정의 (User, Board, Post, Tag, Comment, Reaction) → 변경은 팀 합의 후
├── auth_utils.py        # JWT + 비밀번호 해싱 + get_current_user (나희 작성, 전원 사용)
├── post_utils.py        # 게시글 응답 변환 + 페이지네이션 (재윤 작성, 목록/검색/상세 공용)
├── requirements.txt
├── schemas/             # 요청/응답 Pydantic 스키마 (담당자별 파일)
│   ├── auth.py  comment.py  reaction.py    # 나희
│   ├── board.py                            # 서현
│   ├── post.py                             # 하은
│   ├── search.py                           # 준모
│   └── common.py                           # 재윤 (Page, UtcDateTime)
└── routers/             # API 엔드포인트 (담당자별 파일)
    ├── auth.py  comments.py  reactions.py  # 나희
    ├── boards.py                           # 서현
    ├── posts.py                            # 하은
    ├── search.py                           # 준모
    └── tags.py                             # 재윤
```

## 협업 규칙

- **자기 담당 파일만 수정**합니다. 공통 파일(`main.py`, `database.py`, `models.py`)은 이미 완성되어 있어 건드릴 일이 없고, 바꿔야 하면 팀 합의 후 수정합니다.
- 게시글 목록 응답을 조립하는 코드는 `post_utils.py` 한 곳에 모여 있습니다. 목록에 필드를 추가할 일이 생기면
  `boards.py`와 `search.py`를 각각 고치지 말고 `post_utils.py`만 고치면 양쪽에 함께 반영됩니다.
- 로그인이 필요한 API는 파라미터에 `user: User = Depends(get_current_user)`만 추가하면 됩니다 (`auth_utils.py` 상단 주석 참고).

## API 개요

| 메서드 | 경로 | 설명 | 담당 |
|--------|------|------|------|
| POST | `/auth/signup` | 회원가입 (성공 시 토큰 발급 = 자동 로그인) | 나희 |
| POST | `/auth/login` | 로그인 | 나희 |
| GET | `/auth/me` | 내 정보 조회 (토큰 필요) | 나희 |
| GET | `/boards` | 게시판 목록 | 서현 |
| GET | `/boards/{id}/posts` | 게시판별 게시글 리스트 (최신순, `page`/`size`) | 서현 |
| POST | `/posts` | 게시글 작성 (태그 최대 3개, 익명 선택) | 하은 |
| GET | `/posts/{id}` | 게시글 상세 | 하은 |
| PUT / DELETE | `/posts/{id}` | 게시글 수정/삭제 (작성자만) | 하은 |
| GET | `/search?board_id=&keyword=&tags=` | 검색 + 태그 필터 (AND 조건, `page`/`size`) | 준모 |
| GET / POST | `/posts/{id}/comments` | 댓글 목록/작성 | 나희 |
| DELETE | `/posts/{id}/comments/{cid}` | 댓글 삭제 (작성자만) | 나희 |
| POST | `/posts/{id}/reaction` | 게시글 좋아요/싫어요 | 나희 |
| POST | `/comments/{id}/reaction` | 댓글 좋아요/싫어요 | 나희 |
| GET | `/tags` | 태그 목록 (기본 태그 + 사용된 태그) | 재윤 |

### 목록 응답 형태

게시글 목록(`/boards/{id}/posts`)과 검색(`/search`)은 같은 형태로 응답합니다. (`schemas/common.py`의 `Page`)

```json
{
  "items": [ ... PostListItem ... ],
  "page": 1,
  "size": 10,
  "total_pages": 3,
  "total_elements": 27
}
```

- `page`는 1부터 시작하고, 범위를 넘기면 마지막 페이지로 맞춰서 돌려줍니다.
- `size` 기본값은 10, 최대 50입니다.
- `/search`의 `tags`는 `?tags=시험&tags=과제`(키 반복)가 기본이고 `?tags=시험,과제`(콤마)도 받습니다.

### 게시글 응답 공통 필드

목록·상세 응답에는 프론트 화면을 그리는 데 필요한 아래 필드가 함께 들어갑니다.

| 필드 | 설명 |
|------|------|
| `is_mine` | 작성자 본인 여부. 익명 글은 `author_nickname`이 "익명"이라 프론트가 판별할 수 없어 서버가 내려줍니다 (수정/삭제 버튼 노출용) |
| `my_reaction` | 내가 누른 반응(`"like"` / `"dislike"` / `null`). 새로고침해도 눌린 상태를 유지하는 데 씁니다 |
| `board_id` | 상세에서 목록으로 돌아가거나 태그를 눌러 필터링된 목록으로 이동할 때 씁니다 |
| `comment_count` | 리스트 카드의 댓글 수 |
| `created_at` | UTC임을 명시한 ISO 8601 문자열(`"2026-08-19T04:26:23.685479Z"`). 타임존을 빼고 보내면 브라우저가 로컬 시간으로 읽어 시차만큼 어긋납니다 |

`is_mine`과 `my_reaction`은 로그인했을 때만 채워집니다. 비로그인 조회도 가능하며 이때는 각각 `false` / `null`입니다.

## DB 구조 (models.py)

- **users** — username(아이디), nickname, hashed_password
- **boards** — 자유/새내기/졸업생 게시판
- **posts** — 제목, 본문, 익명 여부, 작성자·게시판 FK
- **tags** + **post_tags** — 태그, 게시글과 다대다 연결 (게시글당 최대 3개는 API에서 검증)
- **comments** — 내용, 익명 여부, 게시글·작성자 FK
- **post_reactions / comment_reactions** — like/dislike, (사용자, 대상) 조합당 1개 제약
