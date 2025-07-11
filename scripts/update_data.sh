#!/bin/bash

echo "=== 威力彩資料更新腳本 ==="

# 檢查是否在正確的目錄
if [ ! -f "backend/crawler.py" ]; then
    echo "❌ 錯誤：請在專案根目錄執行此腳本"
    exit 1
fi

# 進入後端目錄
cd backend

# 啟動虛擬環境
if [ -d "venv" ]; then
    echo "🔧 啟動虛擬環境..."
    source venv/bin/activate
else
    echo "❌ 找不到虛擬環境，請先執行 start_backend.sh"
    exit 1
fi

# 執行爬蟲更新資料
echo "🕷️ 執行爬蟲更新開獎資料..."
python crawler.py

# 執行資料分析
echo "📊 執行資料分析..."
python analyzer.py

echo "✅ 資料更新完成！"