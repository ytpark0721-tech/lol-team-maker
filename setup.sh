#!/bin/bash
set -e

echo ""
echo "====================================="
echo "  LOL Team Maker - 초기 설치"
echo "====================================="

# Python venv
echo "[1/3] 백엔드 패키지 설치..."
cd "$(dirname "$0")/backend"
python3 -m venv venv
./venv/bin/pip install -r requirements.txt -q
echo "  완료"

# Node modules
echo "[2/3] 프론트엔드 패키지 설치..."
cd "$(dirname "$0")/frontend"
npm install --silent
echo "  완료"

# cloudflared
echo "[3/3] cloudflared 설치 (외부 접속용)..."
if ! command -v cloudflared &> /dev/null; then
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -O /tmp/cloudflared.deb
    sudo dpkg -i /tmp/cloudflared.deb
    rm /tmp/cloudflared.deb
    echo "  완료"
else
    echo "  이미 설치됨 ($(cloudflared --version))"
fi

echo ""
echo "설치 완료! 실행하려면:"
echo "  bash start.sh"
echo ""
