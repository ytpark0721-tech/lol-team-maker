#!/bin/bash

# 스크립트 위치 기준 절대경로
ROOT="$(cd "$(dirname "$0")" && pwd)"

# 로컬 IP 출력
IP=$(hostname -I | awk '{print $1}')
echo ""
echo "====================================="
echo "  LOL Team Maker"
echo "====================================="
echo "  로컬:    http://localhost:5174"
echo "  네트워크: http://$IP:5174"
echo "====================================="
echo ""

# 백엔드 실행
cd "$ROOT/backend"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt -q
fi
./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

# 프론트엔드 실행
cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo "백엔드 PID: $BACKEND_PID"
echo "프론트엔드 PID: $FRONTEND_PID"
echo "종료하려면 Ctrl+C"

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
