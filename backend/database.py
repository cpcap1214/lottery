from sqlalchemy.orm import Session
from models import LotteryDraw, AnalysisResult, get_database, create_tables
from datetime import datetime, date
from typing import List, Optional
import json

class DatabaseManager:
    def __init__(self):
        create_tables()
    
    def get_db(self):
        return next(get_database())
    
    def add_lottery_draw(self, period: str, draw_date: date, numbers: List[int], special_number: int) -> bool:
        """新增開獎資料"""
        db = self.get_db()
        try:
            # 檢查是否已存在
            existing = db.query(LotteryDraw).filter(LotteryDraw.period == period).first()
            if existing:
                # 更新現有資料
                existing.draw_date = draw_date
                existing.numbers = numbers
                existing.special_number = special_number
                existing.updated_at = datetime.utcnow()
            else:
                # 建立新資料
                draw = LotteryDraw(
                    period=period,
                    draw_date=draw_date,
                    numbers=numbers,
                    special_number=special_number
                )
                db.add(draw)
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"新增開獎資料錯誤: {e}")
            return False
        finally:
            db.close()
    
    def get_all_draws(self, limit: Optional[int] = None) -> List[LotteryDraw]:
        """取得所有開獎資料"""
        db = self.get_db()
        try:
            query = db.query(LotteryDraw).order_by(LotteryDraw.period.desc())
            if limit:
                query = query.limit(limit)
            return query.all()
        finally:
            db.close()
    
    def get_draws_paginated(self, page: int = 1, limit: int = 10) -> List[LotteryDraw]:
        """取得分頁開獎資料"""
        db = self.get_db()
        try:
            offset = (page - 1) * limit
            return db.query(LotteryDraw).order_by(LotteryDraw.period.desc()).offset(offset).limit(limit).all()
        finally:
            db.close()
    
    def get_total_draws_count(self) -> int:
        """取得開獎資料總數"""
        db = self.get_db()
        try:
            return db.query(LotteryDraw).count()
        finally:
            db.close()
    
    def get_latest_draw(self) -> Optional[LotteryDraw]:
        """取得最新一期開獎資料"""
        db = self.get_db()
        try:
            return db.query(LotteryDraw).order_by(LotteryDraw.period.desc()).first()
        finally:
            db.close()
    
    def get_draws_by_date_range(self, start_date: date, end_date: date) -> List[LotteryDraw]:
        """根據日期範圍取得開獎資料"""
        db = self.get_db()
        try:
            return db.query(LotteryDraw).filter(
                LotteryDraw.draw_date >= start_date,
                LotteryDraw.draw_date <= end_date
            ).order_by(LotteryDraw.period.desc()).all()
        finally:
            db.close()
    
    def save_analysis_result(self, period: str, avoid_numbers: List[int], 
                           frequency_data: dict, gap_analysis: dict, total_periods: int) -> bool:
        """儲存分析結果"""
        db = self.get_db()
        try:
            # 檢查是否已存在
            existing = db.query(AnalysisResult).filter(AnalysisResult.period == period).first()
            if existing:
                # 更新現有分析結果
                existing.avoid_numbers = avoid_numbers
                existing.frequency_data = frequency_data
                existing.gap_analysis = gap_analysis
                existing.total_periods = total_periods
                existing.analysis_date = datetime.utcnow()
            else:
                # 建立新分析結果
                result = AnalysisResult(
                    period=period,
                    avoid_numbers=avoid_numbers,
                    frequency_data=frequency_data,
                    gap_analysis=gap_analysis,
                    total_periods=total_periods
                )
                db.add(result)
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"儲存分析結果錯誤: {e}")
            return False
        finally:
            db.close()
    
    def get_latest_analysis(self) -> Optional[AnalysisResult]:
        """取得最新分析結果"""
        db = self.get_db()
        try:
            return db.query(AnalysisResult).order_by(AnalysisResult.analysis_date.desc()).first()
        finally:
            db.close()
    
    def get_total_draws_count(self) -> int:
        """取得總開獎期數"""
        db = self.get_db()
        try:
            return db.query(LotteryDraw).count()
        finally:
            db.close()

# 全域資料庫管理員實例
db_manager = DatabaseManager()