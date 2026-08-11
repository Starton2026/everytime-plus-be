# 담당: 준모 - 검색 + 태그 필터 스키마
# 검색 결과 목록 응답은 하은의 PostListItem을 재사용한다.
from pydantic import BaseModel


class SearchParams(BaseModel):
    """GET /search 쿼리 파라미터 정리용 (실제론 Query()로 받아도 됨)

    - keyword: 1~50자, 공백만 입력 불가. 제목+본문 검색
    - tags: 다중 선택 가능. 검색어와 AND 조건으로 적용
    """

    keyword: str | None = None
    tags: list[str] = []
    board_id: int | None = None
