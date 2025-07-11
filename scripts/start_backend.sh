#!/bin/bash

echo "=== 威力彩分析系統 - 後端啟動腳本 ==="

# 檢查是否在正確的目錄
if [ ! -f "backend/main.py" ]; then
    echo "❌ 錯誤：請在專案根目錄執行此腳本"
    exit 1
fi

# 進入後端目錄
cd backend

# 檢查 Python 虛擬環境
if [ ! -d "venv" ]; then
    echo "📦 建立 Python 虛擬環境..."
    python3 -m venv venv
fi

# 啟動虛擬環境
echo "🔧 啟動虛擬環境..."
source venv/bin/activate

# 安裝依賴
echo "📥 安裝 Python 依賴..."
pip install -r requirements.txt

# 初始化資料庫
echo "🗄️ 初始化資料庫..."
python setup_db.py

# 啟動 FastAPI 服務
echo "🚀 啟動 FastAPI 服務..."
echo "API 文件：http://localhost:8000/docs"
echo "按 Ctrl+C 停止服務"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000