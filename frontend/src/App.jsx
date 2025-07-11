import { useState, useEffect } from 'react';
import Home from './pages/Home';
import History from './pages/History';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  // 路由處理函數
  const handleRouting = () => {
    const path = window.location.pathname;
    const hash = window.location.hash;
    
    console.log('Current path:', path, 'hash:', hash);
    
    // 支援多種路由格式
    if (path === '/history' || hash === '#/history' || path.includes('history')) {
      console.log('Setting page to history');
      setCurrentPage('history');
    } else {
      console.log('Setting page to home');
      setCurrentPage('home');
    }
  };

  // 初始路由處理
  useEffect(() => {
    handleRouting();
  }, []);

  // 監聽 popstate 事件來處理瀏覽器前進後退
  useEffect(() => {
    const handlePopstate = () => {
      console.log('Popstate event triggered');
      handleRouting();
    };

    window.addEventListener('popstate', handlePopstate);
    return () => window.removeEventListener('popstate', handlePopstate);
  }, []);

  // 監聽 hashchange 事件
  useEffect(() => {
    const handleHashChange = () => {
      console.log('Hash change event triggered');
      handleRouting();
    };

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  // 程式化導航函數
  const navigateTo = (page) => {
    console.log('Navigating to:', page);
    if (page === 'history') {
      window.history.pushState({}, '', '/history');
      setCurrentPage('history');
    } else {
      window.history.pushState({}, '', '/');
      setCurrentPage('home');
    }
  };

  const renderPage = () => {
    console.log('Rendering page:', currentPage);
    switch (currentPage) {
      case 'history':
        return <History navigateTo={navigateTo} />;
      default:
        return <Home navigateTo={navigateTo} />;
    }
  };

  return renderPage();
}

export default App;
