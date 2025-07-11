# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

威力彩號碼分析系統 - 基於台灣彩券歷史開獎資料分析，計算並推薦「下一期最不會開出的號碼」。專案設計考量客戶技術不熟悉、年紀較大，以簡單、穩定、易用、易維護為主要原則。

### 核心功能需求
1. **資料來源處理**
   - 從台灣彩券官網取得威力彩歷史開獎資料（期數、日期、開出號碼）
   - 資料範圍：2024第113001期 到 2025第114054期（7月7日），並持續自動更新
   
2. **核心演算法**
   - 根據歷史資料計算與分析「下一期最不會開出的號碼」
   - 使用頻率統計、間隔期數分析等方法
   
3. **介面功能**
   - 清楚呈現推薦「下期最不會開出的號碼」
   - 提供歷史號碼查詢功能（簡單呈現）
   - 每期自動更新資料與結果

## 技術架構

### 前端 (Frontend)
- **React + Vite**: UI簡潔、容易維護，快速啟動開發
- **Tailwind CSS**: 快速打造乾淨、易讀的介面，客戶易理解
- **Axios**: API 呼叫處理

### 後端 (Backend)  
- **Python + FastAPI**: Python易用於資料分析、爬蟲，FastAPI 易於快速搭建API
- **pandas**: 資料處理與分析
- **requests + BeautifulSoup**: 網頁爬蟲，抓取官網資料

### 資料儲存
- **SQLite**: 本地輕量資料庫，簡單易用且無需額外安裝大型DBMS

### 部署平台
- **Vercel**: React前端部署，免費且快速
- **Render.com**: FastAPI後端部署，SQLite資料庫隨後端同環境部署

## 開發命令

### 前端開發 (React + Vite)
```bash
# 建立前端專案
npm create vite@latest frontend -- --template react
cd frontend

# 安裝依賴
npm install
npm install -D tailwindcss postcss autoprefixer
npm install axios

# 初始化 Tailwind CSS
npx tailwindcss init -p

# 開發模式
npm run dev

# 建構生產版本
npm run build

# 預覽建構結果
npm run preview

# 型別檢查 (如果使用 TypeScript)
npm run type-check

# Lint 檢查
npm run lint
```

### 後端開發 (FastAPI + Python)
```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安裝依賴
pip install fastapi uvicorn pandas requests beautifulsoup4 python-multipart

# 開發模式 (自動重載)
uvicorn main:app --reload --port 8000

# 生產環境
uvicorn main:app --host 0.0.0.0 --port 8000

# 執行爬蟲更新資料
python crawler.py

# 執行資料分析
python analyzer.py

# 建立資料庫
python setup_db.py
```

### 測試命令
```bash
# 前端測試
npm test

# 後端測試
pytest

# 整合測試
python test_integration.py
```

## 專案結構

```
lottery/
├── frontend/                    # React 前端應用
│   ├── src/
│   │   ├── components/         # React 元件
│   │   │   ├── NumberDisplay.jsx    # 號碼顯示元件
│   │   │   ├── HistoryTable.jsx     # 歷史資料表格
│   │   │   └── UpdateButton.jsx     # 更新按鈕
│   │   ├── pages/              # 頁面元件
│   │   │   ├── Home.jsx            # 主頁面
│   │   │   └── History.jsx         # 歷史查詢頁面
│   │   ├── services/           # API 服務
│   │   │   └── api.js              # API 呼叫封裝
│   │   ├── utils/              # 工具函數
│   │   ├── App.jsx             # 主應用元件
│   │   └── main.jsx            # 應用入口
│   ├── public/                 # 靜態資源
│   ├── package.json            # 前端依賴配置
│   ├── vite.config.js          # Vite 配置
│   └── tailwind.config.js      # Tailwind CSS 配置
├── backend/                    # FastAPI 後端
│   ├── main.py                 # FastAPI 主應用
│   ├── models.py               # 資料模型定義
│   ├── database.py             # 資料庫連線與操作
│   ├── crawler.py              # 網頁爬蟲模組
│   ├── analyzer.py             # 資料分析模組
│   ├── scheduler.py            # 定時任務調度
│   ├── utils.py                # 工具函數
│   ├── requirements.txt        # Python 依賴
│   └── tests/                  # 後端測試
├── data/                       # 資料目錄
│   ├── lottery.db              # SQLite 資料庫
│   └── backup/                 # 資料備份
├── docs/                       # 專案文件
└── scripts/                    # 部署與維護腳本
```

## 資料結構設計

### 威力彩開獎資料格式
```json
{
    "期數": "114054",
    "日期": "2025-07-07",
    "開獎號碼": [1, 12, 23, 25, 33, 35],
    "特別號": 5
}
```

### API 端點設計
```bash
# 取得最新一期資料與推薦避免號碼
GET /api/latest-number
# 回應範例:
{
  "latest_period": "114054",
  "latest_date": "2025-07-07",
  "latest_numbers": [1, 12, 23, 25, 33, 35],
  "latest_special": 5,
  "recommended_avoid_numbers": [7, 14, 27, 31, 36, 38],
  "analysis_summary": {
    "total_periods": 500,
    "last_update": "2025-07-07T20:30:00"
  }
}

# 取得歷史開獎資料
GET /api/history?limit=50&offset=0
# 回應範例:
{
  "data": [...],
  "total": 500,
  "page": 1,
  "per_page": 50
}

# 手動觸發資料更新
POST /api/update
# 回應範例:
{
  "success": true,
  "updated_count": 5,
  "last_period": "114059"
}

# 取得號碼統計資料
GET /api/statistics
# 回應範例:
{
  "number_frequency": {...},
  "special_frequency": {...},
  "gap_analysis": {...}
}
```

## 核心演算法實作

### 資料分析流程
1. **頻率統計**: 使用 pandas 計算每個號碼的出現次數和頻率
2. **間隔分析**: 計算各號碼距離上次開出的期數間隔
3. **權重計算**: 結合頻率和間隔，計算號碼被選中的可能性
4. **推薦生成**: 選取分數最低的號碼作為「最不會開出的號碼」

### 演算法範例邏輯
```python
def analyze_avoid_numbers(historical_data):
    # 計算頻率 (出現次數 / 總期數)
    frequency = calculate_frequency(historical_data)
    
    # 計算間隔 (距離上次開出的期數)
    gap_periods = calculate_gap_periods(historical_data)
    
    # 綜合評分 (頻率權重 + 間隔權重)
    scores = {}
    for number in range(1, 39):  # 威力彩號碼範圍 1-38
        freq_score = 1 - frequency.get(number, 0)  # 頻率越低分數越高
        gap_score = gap_periods.get(number, 0) / 100  # 間隔越久分數越高
        scores[number] = freq_score * 0.7 + gap_score * 0.3
    
    # 選取分數最高的 6 個號碼
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:6]
```

## UI/UX 設計原則

### 針對年長使用者的設計考量
- **大字體**: 主要內容使用 18px 以上字體
- **高對比**: 黑底白字或白底黑字，避免灰色文字
- **簡潔介面**: 避免過多互動元素，重點功能明確突出
- **明確標題**: 每個區塊都有清楚的標題說明

### 頁面結構範例
```
|----------------------------------|
| 威力彩最不會開出號碼推薦            |
|----------------------------------|
| 最新一期：2025-07-07（第114054期）   |
| 開獎號碼：01 12 23 25 33 35 + 05   |
|----------------------------------|
| 推薦避免號碼                        |
| [07] [14] [27] [31] [36] [38]      |
|----------------------------------|
| [查看歷史資料] [手動更新]             |
|----------------------------------|
```

## 自動更新機制

### 後端定時任務
- 使用 cron job 或 Python scheduler 每日定時執行
- 爬蟲檢查官網是否有新開獎資料
- 自動更新資料庫並重新計算推薦號碼

### 前端更新策略
- 頁面載入時自動檢查最新資料
- 提供手動更新按鈕供用戶觸發
- 顯示最後更新時間

## 部署配置

### Vercel (前端)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install"
}
```

### Render.com (後端)
```yaml
services:
  - type: web
    name: lottery-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

## 開發注意事項

### 資料爬蟲
- 實作容錯機制處理網路異常
- 資料格式驗證確保正確性
- 遵守網站爬蟲禮儀，避免過於頻繁請求

### 資料驗證
- 開獎號碼範圍檢查 (1-38)
- 期數格式驗證
- 日期合理性檢查

### 錯誤處理
- API 異常回應處理
- 資料庫連線失敗處理
- 前端錯誤邊界設置

### 客戶溝通重點
- **演算法說明簡化**: 「根據歷史資料計算最不常開出的號碼」
- **避免技術細節**: 不提供複雜的統計學解釋
- **結果呈現**: 直接明確的號碼推薦，無需過多解釋