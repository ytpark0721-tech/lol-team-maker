# CLAUDE.md — lol-team-maker

## 프로젝트 개요

**LOL 내전 팀 자동 밸런싱 웹 앱**입니다.
10명의 소환사명을 입력하면 op.gg에서 모스트 챔피언 5개와 역대 최고 티어를 자동 조회하고,
내전 멤버들이 직접 입력한 몸값(1~10)을 기반으로 라인 포지션과 몸값이 균형 잡힌 두 팀을 자동 구성합니다.

---

## 디렉토리 구조

```
lol-team-maker/
├── backend/                    # FastAPI 백엔드
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── database.py             # SQLite 초기화
│   ├── requirements.txt
│   ├── models/
│   │   └── schemas.py          # Pydantic 스키마
│   ├── routers/
│   │   ├── players.py          # 참가자 CRUD + op.gg 조회
│   │   └── teams.py            # 팀 자동 배정
│   └── services/
│       ├── scraper.py          # op.gg 스크래핑 (curl 기반)
│       └── balancer.py         # 팀 밸런싱 알고리즘
├── frontend/                   # React + Vite 프론트엔드
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── components/
│           ├── PlayerInput.jsx  # 소환사명 입력 + op.gg 조회
│           ├── PlayerList.jsx   # 참가자 목록 / 몸값 조정
│           └── TeamResult.jsx   # 팀 결과 출력
├── setup.sh                    # 최초 설치 스크립트
├── start.sh                    # 실행 스크립트
├── 사용설명서.txt
└── CLAUDE.md
```

---

## 기술 스택

- **Backend**: FastAPI, aiosqlite, BeautifulSoup4
- **Frontend**: React, Vite, axios
- **DB**: SQLite (`backend/lol.db`, gitignore됨)
- **포트**: 백엔드 8001, 프론트엔드 5174

---

## op.gg 스크래핑 방식

`backend/services/scraper.py`

op.gg가 클라이언트 사이드 렌더링으로 변경되어 curl + HTML 파싱 방식 사용:

- **모스트 챔피언 5개**: `<meta name="description">` 태그에서 챔피언명 추출
- **역대 최고 티어**: 시즌 기록 테이블 `first-letter:uppercase` 클래스 파싱 후 최고값 선택
- **주 라인**: 챔피언→라인 매핑 딕셔너리로 추론
- **소환사명 형식**: `닉네임#태그` 또는 `닉네임-태그` 모두 지원 (한글 포함 URL 인코딩 처리)

---

## 밸런싱 알고리즘

`backend/services/balancer.py`

1. 주 라인 → 서브 라인 → 나머지 순으로 각 라인에 2명씩 배정
2. 라인별 2명 쌍에서 2⁵ = 32가지 팀 조합을 모두 탐색
3. 양팀 몸값 합산 차이가 최소인 조합 선택

---

## 개발 규칙

- `main` 직접 커밋 금지 (문서 수정만 예외)
- 브랜치: `feature/<이슈번호>-<작업명>`
- 커밋: `<타입>: <변경 내용>` (feat / fix / docs / chore)
- 소스 파일 최대 300줄

---

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | `/players` | 참가자 목록 |
| POST | `/players/scrape?summoner_name=` | op.gg 조회 후 추가 |
| POST | `/players` | 수동 추가 |
| PATCH | `/players/{id}` | 몸값 / 라인 수정 |
| DELETE | `/players/{id}` | 삭제 |
| DELETE | `/players` | 전체 초기화 |
| POST | `/teams/generate` | 팀 자동 배정 |
