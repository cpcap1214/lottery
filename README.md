# 威力彩號碼分析系統

基於台灣彩券威力彩歷史開獎資料的分析系統，推薦「最不會開出的號碼」。

## 功能特色

- 🎯 **智能分析**：基於歷史資料分析，推薦避免選擇的號碼
- 📊 **資料視覺化**：清晰呈現開獎號碼和推薦結果
- 🔄 **自動更新**：支援手動和自動更新開獎資料
- 📱 **響應式設計**：適配電腦、平板、手機各種裝置
- 👴 **長者友善**：大字體、高對比、簡潔介面設計

## 技術架構

### 前端
- **React 18** + **Vite** - 現代化前端框架
- **Tailwind CSS** - 快速樣式開發
- **Axios** - HTTP 請求處理

### 後端
- **FastAPI** - 高效能 Python API 框架
- **SQLAlchemy** - 資料庫 ORM
- **Pandas** - 資料分析處理
- **BeautifulSoup** - 網頁爬蟲

### 資料庫
- **SQLite** - 輕量級本地資料庫

## 快速開始

### 環境需求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 1. 克隆專案
```bash
git clone [專案網址]
cd lottery
```

### 2. 啟動後端服務
```bash
# 使用腳本啟動（推薦）
./scripts/start_backend.sh

# 或手動啟動
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python setup_db.py
uvicorn main:app --reload
```

後端服務將在 http://localhost:8000 啟動
API 文件：http://localhost:8000/docs

### 3. 啟動前端服務
```bash
# 使用腳本啟動（推薦）
./scripts/start_frontend.sh

# 或手動啟動
cd frontend
npm install
npm run dev
```

前端應用將在 http://localhost:5173 啟動

## 開發命令

### 後端開發
```bash
cd backend

# 啟動開發服務
uvicorn main:app --reload

# 初始化資料庫
python setup_db.py

# 執行爬蟲更新資料
python crawler.py

# 執行資料分析
python analyzer.py

# 安裝新依賴
pip install package_name
pip freeze > requirements.txt
```

### 前端開發
```bash
cd frontend

# 啟動開發服務
npm run dev

# 建構生產版本
npm run build

# 預覽建構結果
npm run preview

# 程式碼檢查
npm run lint

# 安裝新依賴
npm install package_name
```

## API 端點

### 主要端點
- `GET /api/latest-number` - 取得最新分析結果
- `GET /api/history` - 取得歷史開獎資料
- `POST /api/update` - 手動更新資料
- `GET /api/statistics` - 取得統計資料
- `POST /api/analyze` - 重新執行分析

### 完整 API 文件
啟動後端服務後，造訪 http://localhost:8000/docs 查看完整 API 文件。

## 專案結構

```
lottery/
├── backend/                    # 後端 FastAPI 應用
│   ├── main.py                 # 主應用入口
│   ├── models.py               # 資料模型
│   ├── database.py             # 資料庫操作
│   ├── crawler.py              # 網頁爬蟲
│   ├── analyzer.py             # 資料分析
│   ├── setup_db.py             # 資料庫初始化
│   └── requirements.txt        # Python 依賴
├── frontend/                   # 前端 React 應用
│   ├── src/
│   │   ├── components/         # React 元件
│   │   ├── pages/              # 頁面元件
│   │   ├── services/           # API 服務
│   │   └── utils/              # 工具函數
│   ├── package.json            # 前端依賴
│   └── tailwind.config.js      # Tailwind 配置
├── data/                       # 資料目錄
│   ├── lottery.db              # SQLite 資料庫
│   └── backup/                 # 資料備份
├── scripts/                    # 輔助腳本
│   ├── start_backend.sh        # 後端啟動腳本
│   ├── start_frontend.sh       # 前端啟動腳本
│   └── update_data.sh          # 資料更新腳本
└── docs/                       # 專案文件
```

## 資料更新

### 手動更新
```bash
# 使用腳本更新（推薦）
./scripts/update_data.sh

# 或通過 API
curl -X POST http://localhost:8000/api/update
```

### 自動更新
可設置 cron job 定期執行資料更新：
```bash
# 每天早上 9 點更新
0 9 * * * /path/to/lottery/scripts/update_data.sh
```

## 部署

### Vercel 部署（一鍵部署）

本專案已配置為可在 Vercel 一鍵部署：

#### 準備工作
確保專案根目錄有以下檔案：
- `vercel.json` - Vercel 設定檔
- `requirements.txt` - Python 套件依賴  
- `package.json` - 專案設定

#### 部署步驟
1. **安裝 Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **登入 Vercel**
   ```bash
   vercel login
   ```

3. **部署專案**
   ```bash
   vercel --prod
   ```

#### 環境變數設定
在 Vercel 控制台設定：
- `PYTHONPATH`: `/var/task/backend`

#### 自訂域名（可選）
在 Vercel 控制台可以設定自訂域名。

## 開發注意事項

### 資料爬蟲
- 請遵守網站使用條款
- 避免過於頻繁的請求
- 實作適當的錯誤處理和重試機制

### 資料分析
- 威力彩為隨機開獎，分析結果僅供參考
- 演算法基於統計學原理，不保證準確性
- 定期檢視和調整分析參數

### UI/UX 設計
- 考量年長使用者需求
- 維持大字體和高對比設計
- 確保功能簡潔明確

## 疑難排解

### 常見問題
1. **後端啟動失敗**：檢查 Python 版本和依賴安裝
2. **前端無法連接後端**：確認 API URL 設置正確
3. **資料爬取失敗**：檢查網路連線和目標網站狀態
4. **分析結果為空**：確認資料庫中有足夠的歷史資料

### 除錯模式
```bash
# 後端除錯
cd backend
python main.py

# 前端除錯
cd frontend
npm run dev -- --debug
```

## 授權

本專案僅供學習和研究使用。請勿用於商業用途。

## 免責聲明

- 本系統分析結果僅供參考
- 威力彩為隨機開獎，過往結果不預測未來趨勢
- 請理性購買彩券，避免過度投注
- 開發者不對任何投注損失負責