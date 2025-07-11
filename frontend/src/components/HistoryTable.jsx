import { useState, useEffect } from 'react';
import { lotteryAPI } from '../services/api';
import NumberDisplay from './NumberDisplay';

const HistoryTable = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [total, setTotal] = useState(0);
  const [debugInfo, setDebugInfo] = useState('');
  const itemsPerPage = 10;

  const fetchHistory = async (page = 1) => {
    setLoading(true);
    setError(null);
    setDebugInfo(`正在獲取第 ${page} 頁資料...`);
    
    try {
      console.log('Fetching history page:', page, 'limit:', itemsPerPage);
      const data = await lotteryAPI.getHistory(page, itemsPerPage);
      
      console.log('History API response:', data);
      setDebugInfo(`成功獲取資料: 共 ${data.total} 期，當前第 ${data.page} 頁，每頁 ${data.per_page} 筆`);
      
      setHistory(data.data);
      setTotal(data.total);
      setTotalPages(Math.ceil(data.total / itemsPerPage));
      setCurrentPage(page);
    } catch (err) {
      console.error('History fetch error:', err);
      setError(err.message);
      setDebugInfo(`錯誤: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setDebugInfo('組件載入中...');
    fetchHistory();
  }, []);

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      fetchHistory(page);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  };

  // 開發模式下顯示調試信息
  const isDev = import.meta.env.DEV;

  if (loading) {
    return (
      <div className="card">
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-lg">載入歷史資料中...</span>
        </div>
        {isDev && (
          <div className="mt-4 p-2 bg-gray-100 rounded text-sm text-gray-600">
            調試: {debugInfo}
          </div>
        )}
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="text-center py-8">
          <div className="text-red-600 text-xl mb-4">❌ {error}</div>
          <button 
            onClick={() => fetchHistory()}
            className="btn-primary"
          >
            重新載入
          </button>
          {isDev && (
            <div className="mt-4 p-2 bg-red-50 rounded text-sm text-red-600">
              調試信息: {debugInfo}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">歷史開獎資料</h2>
        <div className="text-lg text-gray-600">
          共 {total} 期資料
        </div>
      </div>

      {isDev && (
        <div className="mb-4 p-2 bg-blue-50 rounded text-sm text-blue-600">
          調試: {debugInfo} | 當前陣列長度: {history.length}
        </div>
      )}

      {history.length === 0 ? (
        <div className="text-center py-8 text-gray-500 text-xl">
          {total > 0 ? '資料載入中...' : '目前沒有歷史資料'}
        </div>
      ) : (
        <>
          <div className="space-y-4 mb-6">
            {history.map((draw) => (
              <div key={draw.period} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                  <div className="flex-shrink-0">
                    <div className="text-xl font-bold text-gray-800">
                      第 {draw.period} 期
                    </div>
                    <div className="text-lg text-gray-600">
                      {formatDate(draw.draw_date)}
                    </div>
                  </div>
                  
                  <div className="flex-grow">
                    <NumberDisplay 
                      numbers={draw.numbers}
                      special={draw.special_number}
                      type="normal"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* 分頁控制 */}
          {totalPages > 1 && (
            <div className="flex justify-center items-center gap-2 mt-6">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage <= 1}
                className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                上一頁
              </button>
              
              <div className="flex items-center gap-2">
                {[...Array(Math.min(5, totalPages))].map((_, index) => {
                  const page = Math.max(1, currentPage - 2) + index;
                  if (page > totalPages) return null;
                  
                  return (
                    <button
                      key={page}
                      onClick={() => handlePageChange(page)}
                      className={`
                        px-4 py-2 rounded-lg font-semibold text-lg
                        ${page === currentPage 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
                        }
                      `}
                    >
                      {page}
                    </button>
                  );
                })}
              </div>
              
              <div className="text-sm text-gray-600 mx-2">
                第 {currentPage} 頁，共 {totalPages} 頁
              </div>
              
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage >= totalPages}
                className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                下一頁
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default HistoryTable;