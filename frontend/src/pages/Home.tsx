import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">
          Welcome to Smart Crop Advisory! 🌾
        </h1>
        <p className="text-blue-100">
          AI-powered advisory system for small and marginal farmers in India
        </p>
      </div>

      {/* Weather Card */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center">
            <span className="text-2xl mr-2">🌤️</span>
            Weather Update
          </h2>
          <span className="text-sm text-gray-500">Your Location</span>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <span className="text-2xl mb-1 block">🌡️</span>
            <p className="text-2xl font-bold text-gray-900">28°C</p>
            <p className="text-sm text-gray-500">Temperature</p>
          </div>
          <div className="text-center">
            <span className="text-2xl mb-1 block">💧</span>
            <p className="text-2xl font-bold text-gray-900">65%</p>
            <p className="text-sm text-gray-500">Humidity</p>
          </div>
          <div className="text-center">
            <span className="text-2xl mb-1 block">🌧️</span>
            <p className="text-2xl font-bold text-gray-900">0mm</p>
            <p className="text-sm text-gray-500">Rainfall</p>
          </div>
          <div className="text-center">
            <span className="text-2xl mb-1 block">💨</span>
            <p className="text-2xl font-bold text-gray-900">12 km/h</p>
            <p className="text-sm text-gray-500">Wind Speed</p>
          </div>
        </div>
        
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Condition:</strong> Partly Cloudy
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            to="/chatbot"
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <span className="text-2xl">💬</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">AI Chatbot</h3>
            <p className="text-sm text-gray-500">Get crop advice in your language</p>
          </Link>

          <Link
            to="/image-analysis"
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <span className="text-2xl">📷</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Image Analysis</h3>
            <p className="text-sm text-gray-500">Identify diseases and pests</p>
          </Link>

          <Link
            to="/market-prices"
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-yellow-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <span className="text-2xl">📈</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Market Prices</h3>
            <p className="text-sm text-gray-500">Check crop prices and trends</p>
          </Link>

          <Link
            to="/community"
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <span className="text-2xl">👥</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Community</h3>
            <p className="text-sm text-gray-500">Connect with other farmers</p>
          </Link>
        </div>
      </div>

      {/* Today's Advice */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Today's Advice</h2>
        <div className="space-y-3">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900 mb-1">सिंचाई का समय</h3>
                <p className="text-sm text-gray-600">आज शाम 5 बजे के बाद सिंचाई करें</p>
              </div>
              <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                सिंचाई
              </span>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900 mb-1">कीट नियंत्रण</h3>
                <p className="text-sm text-gray-600">पत्तियों की जांच करें और आवश्यकता हो तो छिड़काव करें</p>
              </div>
              <span className="px-2 py-1 text-xs rounded-full bg-red-100 text-red-800">
                कीट नियंत्रण
              </span>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900 mb-1">मौसम चेतावनी</h3>
                <p className="text-sm text-gray-600">कल बारिश की संभावना है, फसल की सुरक्षा करें</p>
              </div>
              <span className="px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800">
                मौसम
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Farm Information */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Farm Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p className="text-sm text-gray-500">Farm Size</p>
            <p className="text-lg font-semibold text-gray-900">2.5 acres</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Main Crops</p>
            <p className="text-lg font-semibold text-gray-900">Wheat, Rice</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Farming Experience</p>
            <p className="text-lg font-semibold text-gray-900">5 years</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;