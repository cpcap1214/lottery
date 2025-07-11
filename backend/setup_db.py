#!/usr/bin/env python3
"""
資料庫初始化腳本
建立資料表並插入測試資料
"""

import os
import sys
from datetime import datetime, date, timedelta
from models import create_tables
from database import db_manager

def create_sample_data():
    """建立範例資料用於測試"""
    print("正在建立範例資料...")
    
    # 範例開獎資料
    sample_draws = [
        {
            'period': '114054',
            'date': date(2025, 7, 7),
            'numbers': [1, 12, 23, 25, 33, 35],
            'special_number': 5
        },
        {
            'period': '114053',
            'date': date(2025, 7, 4),
            'numbers': [3, 8, 19, 22, 28, 37],
            'special_number': 2
        },
        {
            'period': '114052',
            'date': date(2025, 7, 1),
            'numbers': [5, 14, 18, 26, 31, 38],
            'special_number': 7
        },
        {
            'period': '114051',
            'date': date(2025, 6, 28),
            'numbers': [2, 9, 16, 24, 29, 36],
            'special_number': 1
        },
        {
            'period': '114050',
            'date': date(2025, 6, 25),
            'numbers': [4, 11, 17, 21, 30, 34],
            'special_number': 6
        }
    ]
    
    success_count = 0
    for draw in sample_draws:
        try:
            success = db_manager.add_lottery_draw(
                period=draw['period'],
                draw_date=draw['date'],
                numbers=draw['numbers'],
                special_number=draw['special_number']
            )
            if success:
                success_count += 1
                print(f"已新增範例資料: 期數 {draw['period']}")
        except Exception as e:
            print(f"新增範例資料失敗 (期數: {draw['period']}): {e}")
    
    print(f"範例資料建立完成！成功新增 {success_count} 筆資料")
    return success_count

def setup_database():
    """設置資料庫"""
    print("開始初始化資料庫...")
    
    # 建立資料目錄
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"已建立資料目錄: {data_dir}")
    
    # 建立資料表
    try:
        create_tables()
        print("資料表建立成功！")
    except Exception as e:
        print(f"建立資料表失敗: {e}")
        return False
    
    # 檢查是否已有資料
    existing_count = db_manager.get_total_draws_count()
    print(f"現有開獎資料: {existing_count} 筆")
    
    # 如果沒有資料，建立範例資料
    if existing_count == 0:
        create_sample_data()
    else:
        print("資料庫已有資料，跳過範例資料建立")
    
    # 驗證設置
    total_draws = db_manager.get_total_draws_count()
    latest_draw = db_manager.get_latest_draw()
    
    print(f"\n資料庫初始化完成！")
    print(f"總開獎資料: {total_draws} 筆")
    if latest_draw:
        print(f"最新一期: {latest_draw.period} ({latest_draw.draw_date})")
    
    return True

if __name__ == "__main__":
    try:
        success = setup_database()
        if success:
            print("\n✅ 資料庫設置成功！")
            print("你現在可以:")
            print("1. 執行 'python main.py' 啟動 API 服務")
            print("2. 執行 'python crawler.py' 更新開獎資料")
            print("3. 執行 'python analyzer.py' 進行號碼分析")
        else:
            print("\n❌ 資料庫設置失敗！")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 設置過程發生錯誤: {e}")
        sys.exit(1)