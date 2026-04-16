@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo =====================================
echo   LOL Team Maker - 초기 설치 (Windows)
echo =====================================

REM winget 확인
winget --version >nul 2>&1
if errorlevel 1 (
    echo [오류] winget이 없습니다. Windows 10/11 최신 버전으로 업데이트 후 다시 시도하세요.
    pause
    exit /b 1
)

REM Python 확인 및 설치
echo [1/4] Python3 확인...
python --version >nul 2>&1
if errorlevel 1 (
    echo   Python3 설치 중...
    winget install Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements
    echo   완료. 터미널을 재시작하여 다시 실행하세요.
    pause
    exit /b 0
) else (
    echo   이미 설치됨
)

REM Node.js 확인 및 설치
echo [2/4] Node.js 확인...
node --version >nul 2>&1
if errorlevel 1 (
    echo   Node.js 설치 중...
    winget install OpenJS.NodeJS.LTS -e --silent --accept-package-agreements --accept-source-agreements
    echo   완료. 터미널을 재시작하여 다시 실행하세요.
    pause
    exit /b 0
) else (
    echo   이미 설치됨
)

REM 백엔드 패키지 설치
echo [3/4] 백엔드 패키지 설치...
cd backend
python -m venv venv
venv\Scripts\pip install -r requirements.txt -q
cd ..
echo   완료

REM 프론트엔드 패키지 설치
echo [4/4] 프론트엔드 패키지 설치...
cd frontend
call npm install --silent
cd ..
echo   완료

REM cloudflared 설치 (선택)
cloudflared --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [선택] cloudflared 설치 중 (외부 접속용)...
    winget install Cloudflare.cloudflared -e --silent --accept-package-agreements --accept-source-agreements
)

echo.
echo =====================================
echo   설치 완료!
echo   실행하려면: start.bat 더블클릭
echo =====================================
pause
