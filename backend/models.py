from sqlalchemy import Column, Integer, String, Date, JSON, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class LotteryDraw(Base):
    __tablename__ = "lottery_draws"
    
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String(20), unique=True, index=True)  # 期數 例如: "114054"
    draw_date = Column(Date, index=True)  # 開獎日期
    numbers = Column(JSON)  # 開獎號碼 [1, 12, 23, 25, 33, 35]
    special_number = Column(Integer)  # 特別號
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String(20), index=True)  # 對應的期數
    avoid_numbers = Column(JSON)  # 推薦避免號碼 [7, 14, 27, 31, 36, 38]
    frequency_data = Column(JSON)  # 頻率統計資料
    gap_analysis = Column(JSON)  # 間隔分析資料
    total_periods = Column(Integer)  # 分析的總期數
    analysis_date = Column(DateTime, default=datetime.utcnow)

# 資料庫設置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lottery.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """建立所有資料表"""
    Base.metadata.create_all(bind=engine)