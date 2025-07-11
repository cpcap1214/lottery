#!/bin/bash

echo "=== 威力彩專案部署腳本 ==="

# 檢查是否已安裝必要工具
echo "檢查部署環境..."

# 檢查 git
if ! command -v git &> /dev/null; then
    echo "錯誤: 請先安裝 Git"
    exit 1
fi

# 檢查 npm
if ! command -v npm &> /dev/null; then
    echo "錯誤: 請先安裝 Node.js 和 npm"
    exit 1
fi

# 檢查 python
if ! command -v python3 &> /dev/null; then
    echo "錯誤: 請先安裝 Python 3"
    exit 1
fi

echo "✅ 環境檢查完成"

# 前端準備
echo "準備前端部署..."
cd frontend

# 安裝前端依賴
echo "安裝前端依賴..."
npm install

# 建構前端
echo "建構前端..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ 前端建構成功"
else
    echo "❌ 前端建構失敗"
    exit 1
fi

cd ..

# 後端準備
echo "準備後端部署..."
cd backend

# 檢查requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ 找不到 requirements.txt"
    exit 1
fi

echo "✅ 後端準備完成"

cd ..

echo "=== 部署準備完成 ==="
echo ""
echo "接下來請按照以下步驟部署："
echo ""
echo "📦 後端部署到 Render.com："
echo "1. 前往 https://render.com"
echo "2. 連接您的 GitHub 儲存庫"
echo "3. 選擇 'Web Service'"
echo "4. 設置以下配置："
echo "   - Build Command: pip install -r backend/requirements.txt"
echo "   - Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "   - Environment: Python"
echo ""
echo "🌐 前端部署到 Vercel："
echo "1. 前往 https://vercel.com"
echo "2. 導入您的 GitHub 儲存庫"
echo "3. 設置 Framework Preset: 'Vite'"
echo "4. Root Directory: 'frontend'"
echo "5. Build Command: 'npm run build'"
echo "6. Output Directory: 'dist'"
echo ""
echo "⚠️  重要提醒："
echo "1. 後端部署完成後，請更新 vercel.json 中的後端 URL"
echo "2. 更新 frontend/src/services/api.js 中的 API_BASE_URL"
echo "3. 確保 CORS 設置正確"
echo ""
echo "🔗 部署完成後，請測試以下 API："
echo "- GET /health (健康檢查)"
echo "- GET /api/latest-number (最新分析)"
echo "- GET /api/history (歷史資料)" 