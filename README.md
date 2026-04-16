# ⚔️ LOL 내전 팀 메이커

롤 내전 멤버 10명을 입력하면 **라인 포지션 + 몸값**을 기준으로 균형 잡힌 두 팀을 자동으로 구성해주는 웹 앱입니다.

---

## 주요 기능

- 소환사명 입력 시 op.gg에서 자동 조회
  - 모스트 챔피언 5개 (역대 기준)
  - 역대 최고 티어
  - 주 라인 자동 추론
- 참가자별 몸값(1~10) 슬라이더로 조정
- 라인 포지션 + 몸값 균형을 동시에 고려한 팀 자동 배정
- **내전 기록 저장** — 경기 결과(승/패) 기록
- **플레이어 통계** — 게임수, 승률, 평균 몸값, 주 라인

---

## 설치 및 실행

### Windows

> git이 없으면 먼저 설치: https://git-scm.com/download/win

**1단계 — 다운로드**

```
git clone https://github.com/ytpark0721-tech/lol-team-maker.git
```

**2단계 — 설치** (`setup.bat` 더블클릭)

- Python3, Node.js, 필요한 패키지 자동 설치
- 설치 도중 "터미널을 재시작하세요" 메시지가 뜨면 → 창 닫고 `setup.bat` 다시 실행

**3단계 — 실행** (`start.bat` 더블클릭)

- 백엔드/프론트엔드 창이 자동으로 열림
- 브라우저에서 `http://localhost:5174` 접속

---

### Linux / Mac

**1단계 — 다운로드 및 설치**

```bash
git clone https://github.com/ytpark0721-tech/lol-team-maker.git
cd lol-team-maker
bash setup.sh
```

- Python3, Node.js, 패키지, cloudflared 자동 설치 (Ubuntu/Debian 기준)

**2단계 — 실행**

```bash
bash start.sh
```

---

## 접속 주소

| 환경 | 주소 |
|---|---|
| 본인 | `http://localhost:5174` |
| 같은 WiFi | `http://<호스트 IP>:5174` |
| 다른 네트워크 | Cloudflare Tunnel 사용 (아래 참고) |

---

## 사용 방법

### 1. 소환사 추가

- `닉네임#태그` 또는 `닉네임-태그` 형식으로 입력 (예: `Hide on bush#KR1`)
- 추가 버튼 클릭 시 op.gg에서 자동 조회
- 조회 실패 시 **수동 입력** 체크 후 라인 직접 선택

### 2. 몸값 조정

- 각 참가자 슬라이더로 몸값(1~10) 설정
- 라인이 잘못 나오면 드롭다운으로 직접 수정

### 3. 팀 자동 배정

- 10명이 모이면 **팀 자동 배정** 버튼 클릭
- 라인 포지션 + 몸값 균형을 동시에 고려한 최적 팀 구성 결과 표시

### 4. 경기 결과 기록

- 내전 후 앱으로 돌아와서 **팀1 승리 / 팀2 승리** 선택
- **기록 저장** 클릭 → SQLite DB에 저장

### 5. 내전 기록 확인

- 상단 **📊 내전 기록** 탭 클릭
- **경기 히스토리**: 날짜별 결과, 클릭하면 라인별 상세 내용 확인
- **플레이어 통계**: 소환사별 게임수 / 승률 / 평균 몸값 / 주 라인

### 6. 새 내전 시작

- **전체 초기화** 버튼 클릭

---

## 다른 네트워크에서 접속 (Cloudflare Tunnel)

같은 WiFi가 아닌 멤버도 접속 가능하게 하는 방법입니다.

```bash
# 터미널 1: 앱 실행
bash start.sh

# 터미널 2: 터널 생성
cloudflared tunnel --url http://localhost:5174
```

터미널에 출력된 `https://xxxx-xxxx.trycloudflare.com` 주소를 멤버들에게 공유하면 됩니다.

- cloudflared 실행 중에만 주소 유지됨 (종료하면 사라짐)
- 앱 껐다 켤 때마다 주소가 바뀜
- 무료, 별도 계정 불필요

---

## 밸런싱 알고리즘

1. 주 라인 → 서브 라인 → 나머지 순으로 각 라인에 2명씩 배정
2. 라인별 2명 쌍에서 2⁵ = 32가지 팀 조합을 모두 탐색
3. 양팀 몸값 합산 차이가 최소인 조합 선택

---

## 스택

- **Backend**: FastAPI + SQLite
- **Frontend**: React + Vite
- **스크래핑**: subprocess curl + BeautifulSoup
