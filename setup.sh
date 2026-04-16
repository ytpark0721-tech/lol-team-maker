#!/bin/bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "====================================="
echo "  LOL Team Maker - 초기 설치"
echo "====================================="

# OS 패키지 (Ubuntu/Debian 기준)
echo "[1/4] 시스템 패키지 확인..."

if ! command -v python3 &> /dev/null; then
    echo "  python3 설치 중..."
    sudo apt-get update -q && sudo apt-get install -y python3 python3-venv python3-pip -q
fi

if ! command -v node &> /dev/null; then
    echo "  Node.js 설치 중..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - -q
    sudo apt-get install -y nodejs -q
fi

if ! command -v curl &> /dev/null; then
    sudo apt-get install -y curl -q
fi

echo "  완료"

# Python venv
echo "[2/4] 백엔드 패키지 설치..."
cd "$ROOT/backend"
python3 -m venv venv
./venv/bin/pip install -r requirements.txt -q
echo "  완료"

# Node modules
echo "[3/4] 프론트엔드 패키지 설치..."
cd "$ROOT/frontend"
npm install --silent
echo "  완료"

# cloudflared
echo "[4/4] cloudflared 설치 (외부 접속용)..."
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
