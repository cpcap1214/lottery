import axios from 'axios';

// 根據環境決定API基礎URL
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://lottery-backend-dhl6.onrender.com'  // 生產環境 - 請替換為實際的Render URL
  : 'http://localhost:8000';  // 開發環境

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 請求攔截器
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// 回應攔截器
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.config?.url, error.message);
    return Promise.reject(error);
  }
);

// API方法
export const lotteryAPI = {
  // 取得最新分析結果
  getLatestAnalysis: () => api.get('/api/latest-number'),
  
  // 取得歷史資料
  getHistory: (page = 1, limit = 10) => 
    api.get(`/api/history?page=${page}&limit=${limit}`),
  
  // 手動更新資料
  updateData: () => api.post('/api/update'),
  
  // 取得統計資料
  getStatistics: () => api.get('/api/statistics'),
  
  // 健康檢查
  healthCheck: () => api.get('/health'),
};

export default api;