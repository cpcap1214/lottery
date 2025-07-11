import HistoryTable from '../components/HistoryTable';
import PropTypes from 'prop-types';

const History = ({ navigateTo }) => {
  const handleBackClick = () => {
    if (navigateTo) {
      navigateTo('home');
    } else {
      // 備用方案
      window.location.hash = '';
      window.location.reload();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* 頁面標題 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            威力彩歷史開獎資料
          </h1>
          <p className="text-xl text-gray-600">
            查看所有歷史開獎結果
          </p>
        </div>

        {/* 返回首頁按鈕 */}
        <div className="text-center mb-6">
          <button
            onClick={handleBackClick}
            className="btn-secondary"
          >
            ← 返回首頁
          </button>
        </div>

        {/* 歷史資料表格 */}
        <HistoryTable />
      </div>
    </div>
  );
};

History.propTypes = {
  navigateTo: PropTypes.func
};

export default History;