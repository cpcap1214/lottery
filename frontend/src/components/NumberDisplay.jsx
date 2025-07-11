import PropTypes from 'prop-types';

const NumberDisplay = ({ numbers, special, title, type = 'normal' }) => {
  const getNumberBoxClass = (type) => {
    switch (type) {
      case 'avoid':
        return 'number-box-avoid';
      case 'likely':
        return 'bg-green-100 border-2 border-green-300 text-green-800 rounded-lg p-4 text-center font-bold text-2xl min-w-[60px] min-h-[60px] flex items-center justify-center';
      case 'special':
        return 'bg-yellow-100 border-2 border-yellow-300 text-yellow-800 rounded-lg p-4 text-center font-bold text-2xl min-w-[60px] min-h-[60px] flex items-center justify-center';
      default:
        return 'number-box';
    }
  };

  const formatNumber = (num) => {
    return num.toString().padStart(2, '0');
  };

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-2xl font-bold mb-4 text-center text-gray-800">
          {title}
        </h3>
      )}
      
      <div className="flex flex-wrap justify-center gap-3 mb-4">
        {numbers?.map((number, index) => (
          <div
            key={index}
            className={getNumberBoxClass(type)}
          >
            {formatNumber(number)}
          </div>
        ))}
        
        {special !== undefined && special !== null && (
          <>
            <div className="flex items-center mx-2">
              <span className="text-3xl font-bold text-gray-600">+</span>
            </div>
            <div className={getNumberBoxClass('special')}>
              {formatNumber(special)}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

NumberDisplay.propTypes = {
  numbers: PropTypes.arrayOf(PropTypes.number).isRequired,
  special: PropTypes.number,
  title: PropTypes.string,
  type: PropTypes.oneOf(['normal', 'avoid', 'likely', 'special'])
};

export default NumberDisplay;