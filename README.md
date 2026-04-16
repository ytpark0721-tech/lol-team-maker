# LOL Team Maker

롤 내전 팀 자동 밸런싱 시스템

## 개요

10명의 내전 참가자를 입력하면 라인 포지션과 몸값을 기반으로 균형 잡힌 두 팀을 자동으로 구성해주는 웹 앱입니다.

## 주요 기능

- 소환사명 입력 시 op.gg에서 주 라인 및 챔피언 폭 자동 조회
- 참가자별 몸값(1~10점) 직접 입력
- 라인 포지션(탑/정글/미드/원딜/서폿) 커버 가능하도록 팀 구성
- 양팀 몸값 합산이 최대한 균등하도록 밸런싱 알고리즘 적용
- 팀 구성 결과 시각화

## 스택

- **Backend**: FastAPI (Python)
- **Frontend**: React
- **DB**: SQLite
- **데이터**: op.gg 스크래핑 (또는 Riot 공식 API)

## 프로젝트 구조

```
lol-team-maker/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   ├── players.py      # 참가자 관리
│   │   └── teams.py        # 팀 구성 / 밸런싱
│   ├── services/
│   │   ├── scraper.py      # op.gg 데이터 조회
│   │   └── balancer.py     # 팀 밸런싱 알고리즘
│   ├── models/
│   │   └── schemas.py
│   └── database.py
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── PlayerInput.jsx     # 참가자 입력
│       │   ├── PlayerList.jsx      # 참가자 목록 / 몸값 설정
│       │   └── TeamResult.jsx      # 팀 결과 출력
│       └── App.jsx
└── README.md
```

## 사용 흐름

1. 소환사명 10명 입력
2. op.gg에서 주 라인, 챔피언 폭 자동 조회
3. 각 참가자 몸값(1~10) 입력
4. "팀 짜기" 버튼 클릭
5. 밸런스 맞춘 팀 1 / 팀 2 결과 출력

## 밸런싱 알고리즘

- 각 팀은 탑/정글/미드/원딜/서폿 1명씩 구성
- 참가자의 주 라인 우선 배정, 서브 라인 차선 배정
- 전체 경우의 수 중 양팀 몸값 합산 차이가 최소인 조합 선택

## 시작하기

```bash
# 백엔드
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 프론트엔드
cd frontend
npm install
npm run dev
```

`http://localhost:5173` 접속
