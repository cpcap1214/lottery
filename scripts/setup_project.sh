#!/bin/bash

echo "=== 威力彩分析系統 - 專案初始化腳本 ==="

# 檢查是否在專案根目錄
if [ ! -f "CLAUDE.md" ]; then
    echo "❌ 錯誤：請在專案根目錄執行此腳本"
    exit 1
fi

echo "🚀 開始初始化威力彩分析系統..."
echo ""

# 1. 設置後端
echo "📦 設置後端環境..."
cd backend

# 建立虛擬環境
if [ ! -d "venv" ]; then
    echo "建立 Python 虛擬環境..."
    python3 -m venv venv
fi

# 啟動虛擬環境
echo "啟動虛擬環境..."
source venv/bin/activate

# 安裝依賴
echo "安裝 Python 依賴..."
pip install -r requirements.txt

# 初始化資料庫
echo "初始化資料庫..."
python setup_db.py

cd ..

# 2. 設置前端
echo ""
echo "🎨 設置前端環境..."
cd frontend

# 安裝依賴
echo "安裝 Node.js 依賴..."
npm install

cd ..

echo ""
echo "✅ 專案初始化完成！"
echo ""
echo "🎯 接下來你可以："
echo "1. 啟動後端服務：./scripts/start_backend.sh"
echo "2. 啟動前端服務：./scripts/start_frontend.sh"
echo "3. 更新開獎資料：./scripts/update_data.sh"
echo ""
echo "📖 更多資訊請查看 README.md"