#!/bin/bash

echo "🚀 快速設置 GitHub 和 Vercel"
echo "============================="

# 詢問用戶信息
read -p "請輸入您的 GitHub 用戶名: " username
read -p "請輸入儲存庫名稱 (預設: lottery-analysis): " repo_name

# 設置預設值
if [ -z "$repo_name" ]; then
    repo_name="lottery-analysis"
fi

# 構建 GitHub URL
github_url="https://github.com/$username/$repo_name.git"

echo ""
echo "📋 將設置以下儲存庫："
echo "   $github_url"
echo ""

# 確認
read -p "確認設置嗎？(y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "已取消設置"
    exit 1
fi

# 設置 remote 並推送
echo "🔗 設置 GitHub remote..."
git remote add origin "$github_url"

echo "📤 推送程式碼到 GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ 程式碼已成功推送到 GitHub!"
    echo ""
    echo "🌐 現在可以在 Vercel 部署了："
    echo "1. 前往 https://vercel.com"
    echo "2. 使用 GitHub 帳號登入"
    echo "3. 點擊 'New Project'"
    echo "4. 選擇儲存庫: $username/$repo_name"
    echo "5. 設置配置："
    echo "   - Framework: Vite"
    echo "   - Root Directory: frontend"
    echo "   - Build Command: npm run build"
    echo "   - Output Directory: dist"
    echo "6. 點擊 'Deploy'"
    echo ""
    echo "🎉 完成！"
else
    echo "❌ 推送失敗，請檢查："
    echo "1. GitHub 儲存庫是否已創建"
    echo "2. 用戶名和儲存庫名稱是否正確"
    echo "3. 是否有推送權限"
fi 