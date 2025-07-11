import { useState, useEffect } from 'react';
import Home from './pages/Home';
import History from './pages/History';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  // 簡單的路由處理
  useEffect(() => {
    const path = window.location.pathname;
    if (path === '/history') {
      setCurrentPage('history');
    } else {
      setCurrentPage('home');
    }
  }, []);

  // 監聽 popstate 事件來處理瀏覽器前進後退
  useEffect(() => {
    const handlePopstate = () => {
      const path = window.location.pathname;
      if (path === '/history') {
        setCurrentPage('history');
      } else {
        setCurrentPage('home');
      }
    };

    window.addEventListener('popstate', handlePopstate);
    return () => window.removeEventListener('popstate', handlePopstate);
  }, []);

  const renderPage = () => {
    switch (currentPage) {
      case 'history':
        return <History />;
      default:
        return <Home />;
    }
  };

  return renderPage();
}

export default App;
