from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
import uvicorn

import os
import sys

# 將 backend 目錄加到 Python 路徑
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from database import db_manager
from crawler import crawler
from analyzer import analyzer
from models import create_tables

# 建立 FastAPI 應用
app = FastAPI(
    title="威力彩號碼分析 API",
    description="基於歷史開獎資料分析並推薦最不會開出的號碼",
    version="1.0.0"
)

# 設置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應該設置具體的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 資料模型
class LotteryDrawResponse(BaseModel):
    period: str
    draw_date: str
    numbers: List[int]
    special_number: int

class LatestAnalysisResponse(BaseModel):
    latest_period: str
    latest_date: str
    latest_numbers: List[int]
    latest_special: int
    recommended_avoid_numbers: List[int]
    recommended_avoid_sets: List[List[int]]
    recommended_likely_numbers: List[int]
    recommended_likely_sets: List[List[int]]
    analysis_summary: dict

class HistoryResponse(BaseModel):
    data: List[LotteryDrawResponse]
    total: int
    page: int
    per_page: int

class UpdateResponse(BaseModel):
    success: bool
    message: str
    updated_count: int
    last_period: Optional[str] = None

class StatisticsResponse(BaseModel):
    total_periods: int
    number_frequency: dict
    special_frequency: dict
    average_frequency: float
    date_range: dict

# 初始化資料庫
@app.on_event("startup")
async def startup_event():
    """應用啟動時初始化資料庫"""
    print("開始初始化資料庫...")
    try:
        create_tables()
        print("資料庫初始化完成")
        
        # 簡單檢查資料庫連線
        total_draws = db_manager.get_total_draws_count()
        print(f"資料庫現有開獎資料: {total_draws} 筆")
        
        if total_draws == 0:
            print("資料庫為空，需要手動更新資料或載入範例資料")
            # 只載入範例資料，不執行爬蟲
            try:
                from setup_db import create_sample_data
                sample_count = create_sample_data()
                print(f"已載入 {sample_count} 筆範例資料")
            except Exception as e:
                print(f"載入範例資料失敗: {e}")
        
        print("啟動完成")
        
    except Exception as e:
        print(f"啟動時發生錯誤: {e}")
        # 不要讓錯誤阻止服務啟動

# API 端點
@app.get("/", summary="根路徑")
async def root():
    """API 根路徑"""
    return {
        "message": "威力彩號碼分析 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/latest-number", response_model=LatestAnalysisResponse, summary="取得最新分析結果")
async def get_latest_analysis():
    """取得最新一期資料與推薦避免號碼"""
    try:
        # 取得最新開獎資料
        latest_draw = db_manager.get_latest_draw()
        if not latest_draw:
            raise HTTPException(status_code=404, detail="找不到開獎資料")
        
        # 取得最新分析結果
        analysis = analyzer.get_latest_analysis()
        analysis_result = None
        if not analysis:
            # 如果沒有分析結果，立即進行分析
            print("沒有找到分析結果，正在進行新分析...")
            analysis_result = analyzer.analyze_avoid_numbers()
            if analysis_result:
                analysis = {
                    'avoid_numbers': analysis_result['avoid_number_sets'][0],  # 第一組作為主要推薦
                    'total_periods': analysis_result['total_periods'],
                    'analysis_date': analysis_result['analysis_date']
                }
        
        if not analysis:
            raise HTTPException(status_code=500, detail="無法產生分析結果")
        
        # 如果沒有完整分析結果，重新進行分析以獲取所有組合
        if not analysis_result:
            analysis_result = analyzer.analyze_avoid_numbers()
        
        avoid_sets = analysis_result['avoid_number_sets'] if analysis_result else [analysis['avoid_numbers']]
        likely_sets = analysis_result['likely_number_sets'] if analysis_result else []
        
        return LatestAnalysisResponse(
            latest_period=latest_draw.period,
            latest_date=latest_draw.draw_date.isoformat(),
            latest_numbers=latest_draw.numbers,
            latest_special=latest_draw.special_number,
            recommended_avoid_numbers=analysis['avoid_numbers'],
            recommended_avoid_sets=avoid_sets,
            recommended_likely_numbers=likely_sets[0] if likely_sets else [],
            recommended_likely_sets=likely_sets,
            analysis_summary={
                "total_periods": analysis['total_periods'],
                "last_update": analysis['analysis_date']
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得分析結果失敗: {str(e)}")

@app.get("/api/history", response_model=HistoryResponse, summary="取得歷史開獎資料")
async def get_history(page: int = 1, limit: int = 10):
    """取得歷史開獎資料"""
    try:
        # 取得總數
        total = db_manager.get_total_draws_count()
        
        # 取得分頁資料
        draws = db_manager.get_draws_paginated(page=page, limit=limit)
        
        # 轉換為回應格式
        draw_responses = []
        for draw in draws:
            draw_responses.append(LotteryDrawResponse(
                period=draw.period,
                draw_date=draw.draw_date.isoformat(),
                numbers=draw.numbers,
                special_number=draw.special_number
            ))
        
        return HistoryResponse(
            data=draw_responses,
            total=total,
            page=page,
            per_page=limit
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得歷史資料失敗: {str(e)}")

@app.post("/api/update", response_model=UpdateResponse, summary="手動更新資料")
async def manual_update(background_tasks: BackgroundTasks):
    """手動觸發資料更新"""
    try:
        # 執行爬蟲更新
        print("開始手動更新資料...")
        result = crawler.update_database(max_pages=3)
        
        # 背景執行分析
        background_tasks.add_task(run_analysis)
        
        # 取得最新期數
        latest_draw = db_manager.get_latest_draw()
        last_period = latest_draw.period if latest_draw else None
        
        return UpdateResponse(
            success=True,
            message="資料更新完成",
            updated_count=result.get('added_count', 0),
            last_period=last_period
        )
    
    except Exception as e:
        return UpdateResponse(
            success=False,
            message=f"更新失敗: {str(e)}",
            updated_count=0
        )

@app.get("/api/statistics", response_model=StatisticsResponse, summary="取得統計資料")
async def get_statistics():
    """取得號碼統計資料"""
    try:
        stats = analyzer.get_statistics()
        if not stats:
            raise HTTPException(status_code=404, detail="沒有統計資料")
        
        return StatisticsResponse(**stats)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得統計資料失敗: {str(e)}")

@app.post("/api/analyze", summary="重新執行分析")
async def run_analysis_endpoint():
    """手動觸發重新分析"""
    try:
        result = analyzer.analyze_avoid_numbers()
        if result:
            return {
                "success": True,
                "message": "分析完成",
                "avoid_number_sets": result['avoid_number_sets'],
                "likely_number_sets": result['likely_number_sets'],
                "total_periods": result['total_periods']
            }
        else:
            raise HTTPException(status_code=500, detail="分析失敗")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗: {str(e)}")

# 背景任務函數
async def run_analysis():
    """背景執行分析任務"""
    try:
        print("背景執行分析任務...")
        analyzer.analyze_avoid_numbers()
        print("背景分析完成")
    except Exception as e:
        print(f"背景分析失敗: {e}")

# 健康檢查端點
@app.get("/health", summary="健康檢查")
async def health_check():
    """API 健康檢查"""
    try:
        # 檢查資料庫連線
        total_draws = db_manager.get_total_draws_count()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "total_draws": total_draws
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )