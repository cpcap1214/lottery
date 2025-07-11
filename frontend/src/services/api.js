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
  getLatestAnalysis: async () => {
    try {
      const response = await api.get('/api/latest-number');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || '取得最新分析失敗');
    }
  },
  
  // 取得歷史資料
  getHistory: async (page = 1, limit = 10) => {
    try {
      const response = await api.get(`/api/history?page=${page}&limit=${limit}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || '取得歷史資料失敗');
    }
  },
  
  // 手動更新資料
  updateData: async () => {
    try {
      const response = await api.post('/api/update');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || '更新資料失敗');
    }
  },
  
  // 取得統計資料
  getStatistics: async () => {
    try {
      const response = await api.get('/api/statistics');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || '取得統計資料失敗');
    }
  },
  
  // 健康檢查
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('API 連線失敗');
    }
  },
};

export default api;