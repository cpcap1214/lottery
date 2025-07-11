#!/bin/bash

# 更新後端 URL 腳本
# 使用方法: ./scripts/update-backend-url.sh YOUR_BACKEND_URL

if [ $# -eq 0 ]; then
    echo "請提供您的後端 URL"
    echo "使用方法: ./scripts/update-backend-url.sh https://lottery-backend-xxxx.onrender.com"
    exit 1
fi

BACKEND_URL=$1

echo "正在更新後端 URL 為: $BACKEND_URL"

# 更新 vercel.json
sed -i '' "s|https://your-backend-app.onrender.com|$BACKEND_URL|g" vercel.json

# 更新 frontend/src/services/api.js
sed -i '' "s|https://your-backend-app.onrender.com|$BACKEND_URL|g" frontend/src/services/api.js

echo "✅ 配置更新完成"
echo "請提交更改到 git："
echo "git add ."
echo "git commit -m \"更新後端 URL: $BACKEND_URL\""
echo "git push" 