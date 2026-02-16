import React from 'react';

const MarketPrices: React.FC = () => {
  const crops = [
    { name: 'Wheat', price: '₹2,100', change: '+5%', trend: 'up' },
    { name: 'Rice', price: '₹1,800', change: '-2%', trend: 'down' },
    { name: 'Cotton', price: '₹6,500', change: '+8%', trend: 'up' },
    { name: 'Sugarcane', price: '₹3,200', change: '+1%', trend: 'up' },
    { name: 'Maize', price: '₹1,900', change: '-3%', trend: 'down' },
    { name: 'Soybean', price: '₹4,100', change: '+12%', trend: 'up' }
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Market Prices</h1>
        
        {/* Price Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 className="font-medium text-green-800">Average Price</h3>
            <p className="text-2xl font-bold text-green-600">₹3,267</p>
            <p className="text-sm text-green-600">per quintal</p>
          </div>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-medium text-blue-800">Market Trend</h3>
            <p className="text-2xl font-bold text-blue-600">↗️ Rising</p>
            <p className="text-sm text-blue-600">+3.2% this week</p>
          </div>
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h3 className="font-medium text-purple-800">Best Performer</h3>
            <p className="text-2xl font-bold text-purple-600">Soybean</p>
            <p className="text-sm text-purple-600">+12% increase</p>
          </div>
        </div>
        
        {/* Crop Prices Table */}
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Crop
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Current Price
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Change
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Trend
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Action
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {crops.map((crop, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="text-sm font-medium text-gray-900">{crop.name}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{crop.price}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`text-sm font-medium ${
                      crop.trend === 'up' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {crop.change}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      crop.trend === 'up' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {crop.trend === 'up' ? '↗️ Rising' : '↘️ Falling'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-green-600 hover:text-green-900">
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {/* Market Insights */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h3 className="font-medium text-yellow-800 mb-2">📈 Market Insights</h3>
            <ul className="text-sm text-yellow-700 space-y-1">
              <li>• Wheat prices expected to rise due to increased demand</li>
              <li>• Cotton market showing strong upward trend</li>
              <li>• Rice prices stabilizing after recent fluctuations</li>
              <li>• Soybean demand increasing from export markets</li>
            </ul>
          </div>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-medium text-blue-800 mb-2">💡 Selling Recommendations</h3>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Consider selling wheat at current high prices</li>
              <li>• Hold cotton for potential further gains</li>
              <li>• Monitor rice prices for selling opportunity</li>
              <li>• Soybean prices at 3-month high - good time to sell</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketPrices;