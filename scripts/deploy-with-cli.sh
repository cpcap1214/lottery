#!/bin/bash

echo "🚀 使用 Vercel CLI 部署威力彩系統"
echo "================================="

# 檢查 Vercel CLI 是否已安裝
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI 未安裝，請先執行: npm install -g vercel"
    exit 1
fi

echo "✅ Vercel CLI 已安裝，版本：$(vercel --version)"

# 檢查是否在專案目錄
if [ ! -f "vercel.json" ]; then
    echo "❌ 找不到 vercel.json，請確認在專案根目錄"
    exit 1
fi

# 檢查前端建構
echo "📦 測試前端建構..."
cd frontend
if npm run build; then
    echo "✅ 前端建構成功"
    cd ..
else
    echo "❌ 前端建構失敗"
    exit 1
fi

# 提交最新更改
echo "📝 檢查 Git 狀態..."
if [[ `git status --porcelain` ]]; then
    echo "發現未提交的更改，正在提交..."
    git add .
    git commit -m "準備 Vercel CLI 部署"
    git push
    echo "✅ 已推送到 GitHub"
fi

echo ""
echo "🔐 現在需要登入 Vercel..."
echo "1. 即將開啟瀏覽器進行登入"
echo "2. 請使用您的 GitHub 帳號登入"
echo "3. 登入完成後返回終端機"
echo ""
read -p "按 Enter 繼續..."

# 登入 Vercel
vercel login

echo ""
echo "🌐 開始部署..."
echo "請按照提示完成設置："
echo "- Set up and deploy? [Y/n] → 輸入 Y"
echo "- Which scope? → 選擇您的帳號"
echo "- Link to existing project? [y/N] → 輸入 N"
echo "- What's your project's name? → 輸入 lottery-analysis 或其他名稱"
echo "- In which directory is your code located? → 輸入 ./"
echo ""
read -p "按 Enter 開始部署..."

# 開始部署
vercel --prod

echo ""
echo "🎉 部署完成！"
echo ""
echo "📋 接下來您可以："
echo "1. 查看部署 URL（在上方輸出中）"
echo "2. 測試網站功能"
echo "3. 如有後端，記得更新 API URL"
echo ""
echo "🔄 未來更新部署："
echo "- 修改程式碼後，只需執行：vercel --prod"
echo "- 或者推送到 GitHub，Vercel 會自動部署" 