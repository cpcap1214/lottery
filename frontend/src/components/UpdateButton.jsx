import { useState } from 'react';
import PropTypes from 'prop-types';

const UpdateButton = ({ onUpdate, disabled = false }) => {
  const [isUpdating, setIsUpdating] = useState(false);

  const handleUpdate = async () => {
    if (isUpdating || disabled) return;
    
    setIsUpdating(true);
    try {
      await onUpdate();
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <button
      onClick={handleUpdate}
      disabled={isUpdating || disabled}
      className={`
        btn-primary
        ${(isUpdating || disabled) ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'}
        flex items-center justify-center gap-2
      `}
    >
      {isUpdating ? (
        <>
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
          更新中...
        </>
      ) : (
        <>
          <svg 
            className="w-5 h-5" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" 
            />
          </svg>
          手動更新
        </>
      )}
    </button>
  );
};

UpdateButton.propTypes = {
  onUpdate: PropTypes.func.isRequired,
  disabled: PropTypes.bool
};

export default UpdateButton;