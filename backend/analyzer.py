import pandas as pd
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple
from collections import Counter, defaultdict
from database import db_manager

class LotteryAnalyzer:
    def __init__(self):
        self.number_range = range(1, 39)  # 威力彩號碼範圍 1-38
        self.special_range = range(1, 9)  # 特別號範圍 1-8
    
    def analyze_avoid_numbers(self, analysis_periods: int = None) -> Dict:
        """分析並產生避免號碼推薦"""
        if analysis_periods is None:
            # 使用所有可用的資料
            draws = db_manager.get_all_draws()
            print(f"開始分析所有 {len(draws)} 期的歷史資料...")
        else:
            # 使用指定期數的資料
            draws = db_manager.get_all_draws(limit=analysis_periods)
            print(f"開始分析最近 {analysis_periods} 期的資料...")
        
        if len(draws) < 3:
            print("歷史資料不足，無法進行分析")
            return None
        
        print(f"實際分析 {len(draws)} 期資料")
        
        # 建立資料框架
        df = self._create_dataframe(draws)
        
        # 進行各項分析
        frequency_analysis = self._analyze_frequency(df)
        gap_analysis = self._analyze_gaps(df)
        trend_analysis = self._analyze_trends(df)
        
        # 計算綜合評分
        avoid_numbers = self._calculate_avoid_scores(
            frequency_analysis, gap_analysis, trend_analysis
        )
        
        # 計算可能開出的號碼
        likely_numbers = self._calculate_likely_scores(
            frequency_analysis, gap_analysis, trend_analysis
        )
        
        # 分析特別號
        special_analysis = self._analyze_special_numbers(df)
        
        # 儲存分析結果（只儲存第一組作為主要推薦）
        latest_draw = draws[0] if draws else None
        if latest_draw:
            db_manager.save_analysis_result(
                period=latest_draw.period,
                avoid_numbers=avoid_numbers[0],  # 只儲存第一組作為主要推薦
                frequency_data=frequency_analysis,
                gap_analysis=gap_analysis,
                total_periods=len(draws)
            )
        
        return {
            'avoid_number_sets': avoid_numbers,
            'likely_number_sets': likely_numbers,
            'frequency_analysis': frequency_analysis,
            'gap_analysis': gap_analysis,
            'special_analysis': special_analysis,
            'trend_analysis': trend_analysis,
            'total_periods': len(draws),
            'analysis_date': datetime.now().isoformat()
        }
    
    def _create_dataframe(self, draws) -> pd.DataFrame:
        """將開獎資料轉換為 pandas DataFrame"""
        data = []
        for draw in draws:
            for number in draw.numbers:
                data.append({
                    'period': draw.period,
                    'date': draw.draw_date,
                    'number': number,
                    'special_number': draw.special_number
                })
        
        return pd.DataFrame(data)
    
    def _analyze_frequency(self, df: pd.DataFrame) -> Dict:
        """分析號碼出現頻率"""
        total_periods = df['period'].nunique()
        
        # 計算每個號碼的出現次數
        frequency_count = df['number'].value_counts().to_dict()
        
        # 計算頻率百分比
        frequency_percent = {}
        for number in self.number_range:
            count = frequency_count.get(number, 0)
            frequency_percent[number] = round(count / total_periods * 100, 2)
        
        # 找出最少出現的號碼
        min_frequency = min(frequency_percent.values())
        least_frequent = [num for num, freq in frequency_percent.items() if freq == min_frequency]
        
        return {
            'frequency_count': frequency_count,
            'frequency_percent': frequency_percent,
            'least_frequent': least_frequent,
            'total_periods': total_periods
        }
    
    def _analyze_gaps(self, df: pd.DataFrame) -> Dict:
        """分析號碼間隔期數"""
        periods = sorted(df['period'].unique(), reverse=True)
        gap_data = {}
        
        for number in self.number_range:
            # 找到該號碼出現的所有期數
            number_periods = df[df['number'] == number]['period'].tolist()
            number_periods = sorted(number_periods, reverse=True)
            
            if number_periods:
                # 計算距離最新期的間隔
                latest_period = periods[0]
                last_appeared = number_periods[0]
                
                # 簡單計算間隔（假設期數是連續的）
                try:
                    gap = int(latest_period) - int(last_appeared)
                except ValueError:
                    gap = 0
                
                gap_data[number] = {
                    'last_appeared': last_appeared,
                    'gap_periods': max(0, gap),
                    'total_appearances': len(number_periods)
                }
            else:
                gap_data[number] = {
                    'last_appeared': None,
                    'gap_periods': len(periods),  # 從未出現
                    'total_appearances': 0
                }
        
        # 找出間隔最久的號碼
        max_gap = max(data['gap_periods'] for data in gap_data.values())
        longest_gap = [num for num, data in gap_data.items() if data['gap_periods'] == max_gap]
        
        return {
            'gap_data': gap_data,
            'longest_gap': longest_gap,
            'max_gap_periods': max_gap
        }
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict:
        """分析號碼趨勢"""
        total_periods = len(df['period'].unique())
        recent_periods = min(20, total_periods)  # 根據實際資料調整分析期數
        periods = sorted(df['period'].unique(), reverse=True)[:recent_periods]
        
        recent_df = df[df['period'].isin(periods)]
        
        # 計算最近期數的出現頻率
        recent_frequency = recent_df['number'].value_counts().to_dict()
        
        # 計算冷門號碼（根據資料量調整標準）
        cold_threshold = max(1, recent_periods // 10)  # 動態調整冷門標準
        cold_numbers = []
        for number in self.number_range:
            count = recent_frequency.get(number, 0)
            if count <= cold_threshold:
                cold_numbers.append(number)
        
        return {
            'recent_frequency': recent_frequency,
            'cold_numbers': cold_numbers,
            'analysis_periods': len(periods)
        }
    
    def _calculate_avoid_scores(self, frequency_analysis: Dict, 
                              gap_analysis: Dict, trend_analysis: Dict) -> List[List[int]]:
        """計算綜合評分並推薦10組避免號碼"""
        scores = {}
        
        for number in self.number_range:
            # 頻率分數 (頻率越低分數越高)
            freq_percent = frequency_analysis['frequency_percent'][number]
            freq_score = max(0, 30 - freq_percent)  # 30% 以下才給分
            
            # 間隔分數 (間隔越久分數越高)
            gap_periods = gap_analysis['gap_data'][number]['gap_periods']
            gap_score = min(gap_periods * 2, 50)  # 每期間隔給2分，最高50分
            
            # 趨勢分數 (冷門號碼加分)
            trend_score = 20 if number in trend_analysis['cold_numbers'] else 0
            
            # 綜合評分
            total_score = freq_score * 0.4 + gap_score * 0.4 + trend_score * 0.2
            scores[number] = round(total_score, 2)
        
        # 排序所有號碼
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # 生成10組不同的避免號碼組合
        avoid_number_sets = []
        
        # 第1組：最高分的6個號碼
        avoid_number_sets.append([number for number, score in sorted_scores[:6]])
        
        # 第2組：混合高分和中等分數
        avoid_number_sets.append([number for number, score in sorted_scores[2:8]])
        
        # 第3組：更多中等分數號碼
        avoid_number_sets.append([number for number, score in sorted_scores[4:10]])
        
        # 第4組：間隔最久的號碼優先
        gap_sorted = sorted(self.number_range, 
                           key=lambda x: gap_analysis['gap_data'][x]['gap_periods'], 
                           reverse=True)
        avoid_number_sets.append(gap_sorted[:6])
        
        # 第5組：頻率最低的號碼優先  
        freq_sorted = sorted(self.number_range,
                            key=lambda x: frequency_analysis['frequency_percent'][x])
        avoid_number_sets.append(freq_sorted[:6])
        
        # 第6組：冷門號碼優先
        cold_numbers = trend_analysis['cold_numbers']
        if len(cold_numbers) >= 6:
            avoid_number_sets.append(cold_numbers[:6])
        else:
            # 補充高分號碼
            supplement = [number for number, score in sorted_scores if number not in cold_numbers]
            avoid_number_sets.append(cold_numbers + supplement[:6-len(cold_numbers)])
        
        # 第7組：綜合分數中段的號碼
        avoid_number_sets.append([number for number, score in sorted_scores[6:12]])
        
        # 第8組：隨機組合高分號碼
        import random
        high_score_numbers = [number for number, score in sorted_scores[:15]]
        random.shuffle(high_score_numbers)
        avoid_number_sets.append(high_score_numbers[:6])
        
        # 第9組：平衡各種因素
        balanced = []
        # 2個最高頻率分數
        balanced.extend([number for number, score in sorted_scores[:2]])
        # 2個最高間隔分數
        balanced.extend(gap_sorted[:2])
        # 2個冷門號碼
        balanced.extend(cold_numbers[:2])
        avoid_number_sets.append(balanced)
        
        # 第10組：保守選擇（中等分數）
        avoid_number_sets.append([number for number, score in sorted_scores[8:14]])
        
        # 確保每組都有6個號碼且去重
        final_sets = []
        for i, number_set in enumerate(avoid_number_sets):
            # 去重並排序
            unique_set = sorted(list(set(number_set)))
            # 如果不足6個，從高分號碼中補充
            if len(unique_set) < 6:
                supplement = [num for num, score in sorted_scores if num not in unique_set]
                unique_set.extend(supplement[:6-len(unique_set)])
            final_sets.append(unique_set[:6])
        
        return final_sets
    
    def _calculate_likely_scores(self, frequency_analysis: Dict, 
                               gap_analysis: Dict, trend_analysis: Dict) -> List[List[int]]:
        """計算可能開出的號碼並推薦10組"""
        scores = {}
        
        for number in self.number_range:
            # 頻率分數 (頻率越高分數越高)
            freq_percent = frequency_analysis['frequency_percent'][number]
            freq_score = min(freq_percent * 2, 70)  # 頻率越高分數越高，最高70分
            
            # 間隔分數 (間隔適中的號碼分數高)
            gap_periods = gap_analysis['gap_data'][number]['gap_periods']
            # 間隔1-5期的給高分，間隔太久或太短的給低分
            if gap_periods >= 1 and gap_periods <= 5:
                gap_score = 40
            elif gap_periods >= 6 and gap_periods <= 10:
                gap_score = 30
            elif gap_periods >= 11 and gap_periods <= 15:
                gap_score = 20
            else:
                gap_score = 10
            
            # 趨勢分數 (熱門號碼加分，與避免號碼相反)
            trend_score = 10 if number not in trend_analysis['cold_numbers'] else 0
            
            # 綜合評分
            total_score = freq_score * 0.5 + gap_score * 0.3 + trend_score * 0.2
            scores[number] = round(total_score, 2)
        
        # 排序所有號碼
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # 生成10組不同的號碼組合
        likely_number_sets = []
        
        # 第1組：最高分的6個號碼
        likely_number_sets.append([number for number, score in sorted_scores[:6]])
        
        # 第2組：混合高分和中等分數
        likely_number_sets.append([number for number, score in sorted_scores[2:8]])
        
        # 第3組：更多中等分數號碼
        likely_number_sets.append([number for number, score in sorted_scores[4:10]])
        
        # 第4組：間隔適中的號碼優先 (修改邏輯)
        gap_medium = sorted(self.number_range, 
                           key=lambda x: abs(gap_analysis['gap_data'][x]['gap_periods'] - 3))
        likely_number_sets.append(gap_medium[:6])
        
        # 第5組：頻率最高的號碼優先  
        freq_sorted = sorted(self.number_range,
                            key=lambda x: frequency_analysis['frequency_percent'][x],
                            reverse=True)
        likely_number_sets.append(freq_sorted[:6])
        
        # 第6組：熱門號碼優先 (與避免號碼相反)
        hot_numbers = [num for num in self.number_range if num not in trend_analysis['cold_numbers']]
        if len(hot_numbers) >= 6:
            likely_number_sets.append(hot_numbers[:6])
        else:
            # 補充高分號碼
            supplement = [number for number, score in sorted_scores if number not in hot_numbers]
            likely_number_sets.append(hot_numbers + supplement[:6-len(hot_numbers)])
        
        # 第7組：綜合分數中段的號碼
        likely_number_sets.append([number for number, score in sorted_scores[6:12]])
        
        # 第8組：隨機組合高分號碼
        import random
        high_score_numbers = [number for number, score in sorted_scores[:15]]
        random.shuffle(high_score_numbers)
        likely_number_sets.append(high_score_numbers[:6])
        
        # 第9組：平衡各種因素
        balanced = []
        # 2個最高頻率分數
        balanced.extend([number for number, score in sorted_scores[:2]])
        # 2個最高間隔分數
        balanced.extend(gap_medium[:2])
        # 2個熱門號碼
        balanced.extend(hot_numbers[:2])
        likely_number_sets.append(balanced)
        
        # 第10組：保守選擇（中等分數）
        likely_number_sets.append([number for number, score in sorted_scores[8:14]])
        
        # 確保每組都有6個號碼且去重
        final_sets = []
        for i, number_set in enumerate(likely_number_sets):
            # 去重並排序
            unique_set = sorted(list(set(number_set)))
            # 如果不足6個，從高分號碼中補充
            if len(unique_set) < 6:
                supplement = [num for num, score in sorted_scores if num not in unique_set]
                unique_set.extend(supplement[:6-len(unique_set)])
            final_sets.append(unique_set[:6])
        
        return final_sets
    
    def _analyze_special_numbers(self, df: pd.DataFrame) -> Dict:
        """分析特別號"""
        special_numbers = df['special_number'].dropna().tolist()
        
        if not special_numbers:
            return {'frequency': {}, 'avoid_special': []}
        
        # 頻率分析
        special_frequency = Counter(special_numbers)
        
        # 找出最少出現的特別號
        min_count = min(special_frequency.values()) if special_frequency else 0
        avoid_special = [num for num, count in special_frequency.items() if count == min_count]
        
        return {
            'frequency': dict(special_frequency),
            'avoid_special': avoid_special[:2]  # 推薦避免前2個
        }
    
    def get_latest_analysis(self) -> Dict:
        """取得最新的分析結果"""
        analysis = db_manager.get_latest_analysis()
        if not analysis:
            return None
        
        return {
            'period': analysis.period,
            'avoid_numbers': analysis.avoid_numbers,
            'frequency_data': analysis.frequency_data,
            'gap_analysis': analysis.gap_analysis,
            'total_periods': analysis.total_periods,
            'analysis_date': analysis.analysis_date.isoformat()
        }
    
    def get_statistics(self) -> Dict:
        """取得統計資料"""
        draws = db_manager.get_all_draws()
        if not draws:
            return {}
        
        df = self._create_dataframe(draws)
        
        # 基本統計
        total_periods = len(draws)
        number_frequency = df['number'].value_counts().to_dict()
        special_frequency = df['special_number'].value_counts().to_dict()
        
        # 號碼出現次數統計
        avg_frequency = sum(number_frequency.values()) / len(number_frequency)
        
        return {
            'total_periods': total_periods,
            'number_frequency': number_frequency,
            'special_frequency': special_frequency,
            'average_frequency': round(avg_frequency, 2),
            'date_range': {
                'start': draws[-1].draw_date.isoformat(),
                'end': draws[0].draw_date.isoformat()
            }
        }

# 建立分析器實例
analyzer = LotteryAnalyzer()

if __name__ == "__main__":
    # 測試分析功能
    result = analyzer.analyze_avoid_numbers()
    if result:
        print(f"推薦避免號碼: {result['avoid_numbers']}")
        print(f"分析期數: {result['total_periods']}")
    else:
        print("分析失敗或資料不足")