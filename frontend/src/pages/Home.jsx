import { useState, useEffect } from 'react';
import { lotteryAPI } from '../services/api';
import NumberDisplay from '../components/NumberDisplay';
import UpdateButton from '../components/UpdateButton';
import PropTypes from 'prop-types';

const Home = ({ navigateTo }) => {
  const [latestData, setLatestData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updateMessage, setUpdateMessage] = useState('');

  const fetchLatestData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await lotteryAPI.getLatestAnalysis();
      setLatestData(data);
    } catch (err) {
      setError(err.message);
      console.error('取得最新資料錯誤:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    setUpdateMessage('');
    try {
      const result = await lotteryAPI.updateData();
      if (result.success) {
        setUpdateMessage(`✅ ${result.message}，更新了 ${result.updated_count} 筆資料`);
        // 重新載入最新資料
        await fetchLatestData();
      } else {
        setUpdateMessage(`❌ ${result.message}`);
      }
    } catch (err) {
      setUpdateMessage(`❌ 更新失敗: ${err.message}`);
    }

    // 3秒後清除訊息
    setTimeout(() => setUpdateMessage(''), 3000);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      weekday: 'short'
    });
  };

  const formatDateTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('zh-TW', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleHistoryClick = () => {
    if (navigateTo) {
      navigateTo('history');
    } else {
      // 備用方案：使用 hash 導航
      window.location.hash = '#/history';
      window.location.reload();
    }
  };

  useEffect(() => {
    fetchLatestData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <div className="text-2xl text-gray-600">載入中...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="card max-w-md w-full mx-4">
          <div className="text-center">
            <div className="text-red-600 text-2xl mb-4">❌ {error}</div>
            <button 
              onClick={fetchLatestData}
              className="btn-primary"
            >
              重新載入
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* 頁面標題 */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            威力彩開獎號碼分析系統
          </h1>
        </div>

        {/* 更新訊息 */}
        {updateMessage && (
          <div className="card mb-6 bg-blue-50 border-blue-200">
            <div className="text-center text-lg font-semibold text-blue-800">
              {updateMessage}
            </div>
          </div>
        )}

        {/* 最新一期開獎資料 */}
        <div className="card mb-8">
          <div className="text-center mb-6">
            <h2 className="text-3xl font-bold text-gray-800 mb-2">
              最新一期開獎結果
            </h2>
            <div className="text-xl text-gray-600">
              第 {latestData?.latest_period} 期 - {formatDate(latestData?.latest_date)}
            </div>
          </div>
          
          <NumberDisplay 
            numbers={latestData?.latest_numbers}
            special={latestData?.latest_special}
            type="normal"
          />
        </div>

        {/* 推薦避免號碼 */}
        <div className="card mb-8">
          <div className="text-center mb-6">
            <h2 className="text-3xl font-bold text-red-700 mb-2">
              下期不會出現的號碼
            </h2>
          </div>
          
          {/* 主要推薦 */}
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">🎯 下期不會出現的號碼</h3>
            <NumberDisplay 
              numbers={latestData?.recommended_avoid_numbers}
              title=""
              type="avoid"
            />
          </div>

          {/* 10組建議 */}
          {latestData?.recommended_avoid_sets && (
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">📊 10組其他號碼建議</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {latestData.recommended_avoid_sets.map((numbers, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-lg">
                    <div className="font-medium text-gray-700 mb-2">
                      第 {index + 1} 組
                      {index === 0 && <span className="ml-2 text-red-600">（主要推薦）</span>}
                      {index === 1 && <span className="ml-2 text-blue-600">（混合策略）</span>}
                      {index === 2 && <span className="ml-2 text-green-600">（中等風險）</span>}
                      {index === 3 && <span className="ml-2 text-purple-600">（間隔優先）</span>}
                      {index === 4 && <span className="ml-2 text-orange-600">（頻率優先）</span>}
                      {index === 5 && <span className="ml-2 text-pink-600">（冷門優先）</span>}
                      {index === 6 && <span className="ml-2 text-indigo-600">（中段選擇）</span>}
                      {index === 7 && <span className="ml-2 text-yellow-600">（隨機組合）</span>}
                      {index === 8 && <span className="ml-2 text-cyan-600">（平衡策略）</span>}
                      {index === 9 && <span className="ml-2 text-gray-600">（保守選擇）</span>}
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {numbers.map((number) => (
                        <span 
                          key={number}
                          className="inline-flex items-center justify-center w-10 h-10 
                                   bg-red-100 text-red-800 font-bold rounded-full text-sm"
                        >
                          {number}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* 分析資訊 */}
        <div className="card mb-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-4">分析資訊</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-lg">
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="font-semibold text-gray-700">分析期數</div>
              <div className="text-2xl font-bold text-blue-600">
                {latestData?.analysis_summary?.total_periods} 期
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="font-semibold text-gray-700">最後更新</div>
              <div className="text-lg text-gray-600">
                {latestData?.analysis_summary?.last_update && 
                  formatDateTime(latestData.analysis_summary.last_update)
                }
              </div>
            </div>
          </div>
        </div>

        {/* 操作按鈕 */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <UpdateButton onUpdate={handleUpdate} />
          
          <button
            onClick={handleHistoryClick}
            className="btn-secondary"
          >
            查看歷史資料
          </button>
        </div>
      </div>
    </div>
  );
};

Home.propTypes = {
  navigateTo: PropTypes.func
};

export default Home;