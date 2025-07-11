#!/bin/bash

echo "=== 威力彩分析系統 - 前端啟動腳本 ==="

# 檢查是否在正確的目錄
if [ ! -f "frontend/package.json" ]; then
    echo "❌ 錯誤：請在專案根目錄執行此腳本"
    exit 1
fi

# 檢查 Node.js 版本
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "⚠️  警告：建議使用 Node.js 18 或更高版本"
    echo "目前版本：$(node -v)"
fi

# 進入前端目錄
cd frontend

# 檢查是否需要安裝依賴
if [ ! -d "node_modules" ]; then
    echo "📥 安裝 Node.js 依賴..."
    npm install
else
    echo "✅ 依賴已安裝"
fi

# 啟動開發服務
echo "🚀 啟動前端開發服務..."
echo "前端網址：http://localhost:5173"
echo "如果遇到錯誤，請檢查後端服務是否已啟動"
echo "按 Ctrl+C 停止服務"
echo ""

npm run dev