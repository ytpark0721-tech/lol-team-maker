@echo off
chcp 65001 >nul
cd /d "%~dp0"

REM 로컬 IP 가져오기
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0.0.1"') do (
    set RAW_IP=%%a
    goto :got_ip
)
:got_ip
set IP=%RAW_IP: =%

echo.
echo =====================================
echo   LOL Team Maker
echo =====================================
echo   로컬:     http://localhost:5174
echo   네트워크:  http://%IP%:5174
echo =====================================
echo   창을 닫으면 앱이 종료됩니다.
echo.

REM 백엔드 실행 (별도 창)
start "LOL-Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8001"

REM 잠깐 대기 후 프론트엔드 실행
timeout /t 2 /nobreak >nul
start "LOL-Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo 브라우저에서 http://localhost:5174 로 접속하세요.
echo.
pause
