# 威力彩號碼分析系統 - 部署指南

本文件提供完整的專案部署指引，包含後端（Render.com）和前端（Vercel）的部署步驟。

## 🎯 部署概述

- **前端**: React + Vite → Vercel
- **後端**: FastAPI + Python → Render.com  
- **資料庫**: SQLite（隨後端部署）

## 📋 部署前準備

### 1. 環境需求
- Node.js 18+ 
- Python 3.11+
- Git
- GitHub 帳號
- Vercel 帳號
- Render.com 帳號

### 2. 檢查專案狀態
```bash
# 執行部署準備腳本
./scripts/deploy.sh
```

## 🔧 Step 1: 後端部署到 Render.com

### 1.1 準備 GitHub 儲存庫
確保您的程式碼已推送到 GitHub：
```bash
git add .
git commit -m "準備部署"
git push origin main
```

### 1.2 建立 Render 服務
1. 前往 [Render.com](https://render.com)
2. 點擊 "New +" → "Web Service"
3. 連接您的 GitHub 儲存庫
4. 選擇 lottery 儲存庫

### 1.3 配置 Render 設定
```
Name: lottery-backend
Environment: Python
Region: Singapore (較接近台灣)
Branch: main
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 1.4 環境變數設定
```
PYTHON_VERSION=3.11
ENVIRONMENT=production
```

### 1.5 健康檢查
```
Health Check Path: /health
```

點擊 "Create Web Service" 開始部署。

### 1.6 取得後端 URL
部署完成後，記下您的後端 URL，格式為：
```
https://lottery-backend-xxxx.onrender.com
```

## 🌐 Step 2: 前端部署到 Vercel

### 2.1 更新 API 配置
使用您剛才取得的後端 URL：

```bash
# 更新 vercel.json
```

更新 `vercel.json` 中的後端 URL：
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://YOUR-BACKEND-URL.onrender.com/api/$1"
    }
  ]
}
```

更新 `frontend/src/services/api.js`：
```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://YOUR-BACKEND-URL.onrender.com'
  : 'http://localhost:8000';
```

### 2.2 建立 Vercel 專案
1. 前往 [Vercel.com](https://vercel.com)
2. 點擊 "New Project"
3. 導入您的 GitHub 儲存庫
4. 選擇 lottery 儲存庫

### 2.3 配置 Vercel 設定
```
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

### 2.4 環境變數設定
```
VITE_API_BASE_URL=https://YOUR-BACKEND-URL.onrender.com
```

點擊 "Deploy" 開始部署。

## 🔍 Step 3: 部署驗證

### 3.1 測試後端 API
```bash
# 健康檢查
curl https://YOUR-BACKEND-URL.onrender.com/health

# 測試最新分析
curl https://YOUR-BACKEND-URL.onrender.com/api/latest-number

# 測試歷史資料
curl https://YOUR-BACKEND-URL.onrender.com/api/history?page=1&limit=5
```

### 3.2 測試前端網站
1. 前往您的 Vercel URL
2. 檢查是否能正常載入頁面
3. 測試號碼顯示功能
4. 測試歷史資料查詢
5. 測試手動更新功能

## 🔄 Step 4: 自動部署設置

### 4.1 GitHub Actions（可選）
如果需要 CI/CD，可以設置 GitHub Actions：

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd frontend && npm install
      - name: Build
        run: cd frontend && npm run build
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

### 4.2 自動更新資料
後端已設置健康檢查，Render 會自動重啟失敗的服務。

## 🐛 常見問題排除

### 問題 1: CORS 錯誤
**症狀**: 前端無法呼叫後端 API  
**解決**: 檢查後端 `main.py` 中的 CORS 設定

### 問題 2: 建構失敗
**症狀**: Vercel 或 Render 建構失敗  
**解決**: 檢查 `package.json` 和 `requirements.txt`

### 問題 3: API 回應慢
**症狀**: 首次呼叫 API 很慢  
**解決**: Render 免費方案會休眠，第一次請求需要等待喚醒

### 問題 4: 資料庫問題
**症狀**: 後端啟動但無資料  
**解決**: 檢查 `setup_db.py` 是否正確執行

## 📊 監控與維護

### 效能監控
- Vercel Analytics（前端）
- Render Metrics（後端）
- 自訂健康檢查端點

### 定期維護
- 每週檢查部署狀態
- 監控 API 回應時間
- 定期備份資料庫

## 🔗 相關連結

- [Vercel 文件](https://vercel.com/docs)
- [Render 文件](https://render.com/docs)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)
- [Vite 部署指南](https://vitejs.dev/guide/build.html)

## 📝 部署清單

- [ ] GitHub 儲存庫建立並推送程式碼
- [ ] Render.com 帳號建立
- [ ] 後端服務部署並取得 URL
- [ ] 更新前端 API 配置
- [ ] Vercel 帳號建立
- [ ] 前端專案部署
- [ ] 測試所有 API 端點
- [ ] 測試前端功能
- [ ] 設置監控
- [ ] 文件更新

完成以上步驟後，您的威力彩號碼分析系統即可正式上線運行！ 