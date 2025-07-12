"""
威力彩爬蟲模組 - 使用 TaiwanLotteryCrawler 獲取真實資料
"""
import ssl
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import requests
from TaiwanLottery import TaiwanLotteryCrawler
from database import db_manager

# 停用SSL警告和驗證
urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class PowerballCrawler:
    def __init__(self):
        """初始化爬蟲"""
        self.setup_ssl_bypass()
        self.crawler = TaiwanLotteryCrawler()
        
    def setup_ssl_bypass(self):
        """設置SSL忽略"""
        # 修補requests的session
        original_request = requests.Session.request
        def patched_request(self, method, url, **kwargs):
            kwargs['verify'] = False
            return original_request(self, method, url, **kwargs)
        requests.Session.request = patched_request
        
        # 修補requests.get
        original_get = requests.get
        def patched_get(url, **kwargs):
            kwargs['verify'] = False
            return original_get(url, **kwargs)
        requests.get = patched_get
    
    def fetch_latest_draws(self, max_pages: int = 5) -> List[Dict]:
        """獲取從2020年到現在的完整威力彩開獎資料"""
        all_draws = []
        
        try:
            print("正在使用 TaiwanLotteryCrawler 獲取威力彩完整歷史資料...")
            
            # 獲取當月資料
            current_data = self.crawler.super_lotto()
            if current_data:
                print(f"成功獲取當月 {len(current_data)} 筆資料")
                parsed_current = self._parse_crawler_data(current_data)
                all_draws.extend(parsed_current)
            
            # 獲取從2020年1月到現在的所有資料
            current_date = date.today()
            start_year = 2020  # 修改為2020年開始
            start_month = 1
            
            # 計算需要獲取的年月組合
            year_month_list = []
            
            # 從2020年1月開始
            for year in range(start_year, current_date.year + 1):
                start_m = start_month if year == start_year else 1
                end_m = current_date.month if year == current_date.year else 12
                
                for month in range(start_m, end_m + 1):
                    # 跳過當月（已經獲取）
                    if year == current_date.year and month == current_date.month:
                        continue
                    year_month_list.append([str(year), f"{month:02d}"])
            
            print(f"準備獲取 {len(year_month_list)} 個月份的歷史資料...")
            
            # 按倒序獲取（從最新的開始）
            year_month_list.reverse()
            
            processed_months = 0
            for year_month in year_month_list:
                try:
                    print(f"獲取 {year_month[0]}-{year_month[1]} 的資料...")
                    monthly_data = self.crawler.super_lotto(year_month)
                    
                    if monthly_data:
                        print(f"成功獲取 {year_month[0]}-{year_month[1]} {len(monthly_data)} 筆資料")
                        parsed_monthly = self._parse_crawler_data(monthly_data)
                        all_draws.extend(parsed_monthly)
                    else:
                        print(f"{year_month[0]}-{year_month[1]} 沒有資料")
                    
                    processed_months += 1
                    
                    # 每獲取5個月的資料就暫停一下，避免請求過快
                    if processed_months % 5 == 0:
                        print(f"已處理 {processed_months} 個月，暫停3秒避免請求過快...")
                        import time
                        time.sleep(3)
                        
                    # 每獲取12個月的資料就顯示進度
                    if processed_months % 12 == 0:
                        print(f"進度: 已處理 {processed_months}/{len(year_month_list)} 個月，目前共 {len(all_draws)} 筆資料")
                        
                except Exception as e:
                    print(f"獲取 {year_month[0]}-{year_month[1]} 資料失敗: {e}")
                    continue
                        
        except Exception as e:
            print(f"TaiwanLotteryCrawler 獲取資料失敗: {e}")
        
        # 按期數排序，最新的在前面
        all_draws.sort(key=lambda x: int(x['period']), reverse=True)
        
        print(f"總共獲取 {len(all_draws)} 筆真實威力彩資料 (從2020年到現在)")
        return all_draws
    
    def _parse_crawler_data(self, data: List[Dict]) -> List[Dict]:
        """解析 TaiwanLotteryCrawler 返回的資料"""
        draws = []
        
        for item in data:
            try:
                # TaiwanLotteryCrawler 的真實資料格式:
                # {'期別': 114000055, '開獎日期': '2025-07-10T00:00:00', '第一區': [1, 2, 7, 14, 28, 31], '第二區': 2}
                period = str(item.get('期別', ''))
                date_str = item.get('開獎日期', '')
                first_area = item.get('第一區', [])  # 一般號碼
                second_area = item.get('第二區', 0)  # 特別號
                
                if not period or not first_area or len(first_area) != 6:
                    print(f"資料不完整，跳過: {item}")
                    continue
                
                # 解析日期
                draw_date = self._parse_date_string(date_str)
                if not draw_date:
                    print(f"日期解析失敗: {date_str}")
                    continue
                
                # 號碼已經是整數列表，直接使用
                regular_numbers = sorted(first_area)
                special_number = int(second_area) if second_area else 1
                
                draws.append({
                    'period': period,
                    'date': draw_date,
                    'numbers': regular_numbers,
                    'special_number': special_number
                })
                
                print(f"解析成功: 期數 {period}, 日期 {draw_date}, 號碼 {regular_numbers}+{special_number}")
                
            except Exception as e:
                print(f"解析單筆資料錯誤: {item}, 錯誤: {e}")
                continue
        
        return draws
    
    def _parse_date_string(self, date_str: str) -> Optional[date]:
        """解析各種格式的日期字串"""
        try:
            # TaiwanLotteryCrawler 回傳的格式: '2025-07-10T00:00:00'
            if 'T' in date_str:
                return datetime.fromisoformat(date_str).date()
            
            # 嘗試其他常見格式
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d']:
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError:
                    continue
            
            print(f"無法解析日期格式: {date_str}")
            return None
            
        except Exception as e:
            print(f"日期解析錯誤: {date_str}, {e}")
            return None
    
    def update_database(self, max_pages: int = 5) -> Dict[str, int]:
        """更新資料庫中的開獎資料"""
        print("開始更新威力彩開獎資料...")
        
        draws_data = self.fetch_latest_draws(max_pages)
        
        if not draws_data:
            print("沒有獲取到任何資料")
            return {'added_count': 0, 'updated_count': 0, 'total_processed': 0}
        
        added_count = 0
        updated_count = 0
        
        for draw in draws_data:
            try:
                success = db_manager.add_lottery_draw(
                    period=draw['period'],
                    draw_date=draw['date'],
                    numbers=draw['numbers'],
                    special_number=draw['special_number']
                )
                
                if success:
                    added_count += 1
                    print(f"已更新期數: {draw['period']}, 日期: {draw['date']}")
                
            except Exception as e:
                print(f"儲存資料錯誤 (期數: {draw['period']}): {e}")
        
        print(f"資料更新完成！新增/更新: {added_count} 筆資料")
        
        return {
            'added_count': added_count,
            'updated_count': updated_count,
            'total_processed': len(draws_data)
        }

# 建立爬蟲實例
crawler = PowerballCrawler()

if __name__ == "__main__":
    # 測試爬蟲
    result = crawler.update_database()
    print(f"爬取結果: {result}")