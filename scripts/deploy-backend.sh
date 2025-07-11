#!/bin/bash

echo "🚀 部署後端到 Render.com"
echo "======================="

# 檢查 Python 環境
echo "🐍 檢查 Python 環境..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ 找不到 Python，請先安裝 Python 3.11+"
    exit 1
fi

echo "✅ 找到 Python: $($PYTHON_CMD --version)"

# 檢查必要文件
echo "📋 檢查必要文件..."
required_files=("backend/main.py" "backend/requirements.txt" "backend/render.yaml")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 找不到 $file"
        exit 1
    fi
done
echo "✅ 所有必要文件都存在"

# 簡單測試後端導入
echo "🧪 測試後端模組導入..."
cd backend
if $PYTHON_CMD -c "
import sys
sys.path.insert(0, '.')
try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    print('✅ FastAPI 相關模組導入成功')
except ImportError as e:
    print(f'❌ 缺少依賴: {e}')
    exit(1)
" 2>/dev/null; then
    echo "✅ 後端核心模組正常"
else
    echo "⚠️  後端依賴可能缺少，部署時 Render 會自動安裝"
fi
cd ..

# 提交最新代碼
echo "📝 提交最新代碼..."
if [[ `git status --porcelain` ]]; then
    git add .
    git commit -m "準備部署後端到 Render.com"
    git push
    echo "✅ 代碼已推送到 GitHub"
else
    echo "✅ 代碼已是最新狀態"
fi

echo ""
echo "🌐 現在請按照以下步驟在 Render.com 部署後端："
echo ""
echo "1. 前往 https://render.com 並登入"
echo "2. 點擊 'New +' → 'Web Service'"
echo "3. 連接您的 GitHub 帳號"
echo "4. 選擇儲存庫: cpcap1214/lottery"
echo "5. 設置以下配置："
echo "   - Name: lottery-backend"
echo "   - Environment: Python"
echo "   - Region: Singapore"
echo "   - Branch: main"
echo "   - Root Directory: backend"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "6. 環境變數："
echo "   - PYTHON_VERSION: 3.11"
echo "   - ENVIRONMENT: production"
echo ""
echo "7. 高級設置："
echo "   - Health Check Path: /health"
echo "   - Auto-Deploy: Yes"
echo ""
echo "8. 點擊 'Create Web Service'"
echo ""
echo "⏳ 部署需要 5-10 分鐘，完成後您會得到一個 URL"
echo "   例如: https://lottery-backend-xxxx.onrender.com"
echo ""
echo "✅ 部署完成後，請執行："
echo "   ./scripts/update-backend-url.sh https://YOUR-ACTUAL-BACKEND-URL.onrender.com"
echo ""
echo "🔗 快速鏈接："
echo "   - Render.com: https://render.com"
echo "   - GitHub 儲存庫: https://github.com/cpcap1214/lottery" 