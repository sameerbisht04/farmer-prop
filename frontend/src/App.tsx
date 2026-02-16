import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Chatbot from './pages/Chatbot';
import ImageAnalysis from './pages/ImageAnalysis';
import MarketPrices from './pages/MarketPrices';
import Community from './pages/Community';
import Profile from './pages/Profile';
import Notifications from './pages/Notifications';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App min-h-screen bg-gray-50">
        <nav className="bg-green-600 text-white p-4">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold">🌾 Smart Crop Advisory</h1>
            <div className="space-x-4">
              <a href="/" className="hover:text-green-200">Home</a>
              <a href="/chatbot" className="hover:text-green-200">Chatbot</a>
              <a href="/image-analysis" className="hover:text-green-200">Image Analysis</a>
              <a href="/market-prices" className="hover:text-green-200">Market Prices</a>
              <a href="/community" className="hover:text-green-200">Community</a>
            </div>
          </div>
        </nav>
        
        <main className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/chatbot" element={<Chatbot />} />
            <Route path="/image-analysis" element={<ImageAnalysis />} />
            <Route path="/market-prices" element={<MarketPrices />} />
            <Route path="/community" element={<Community />} />
            <Route path="/notifications" element={<Notifications />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </main>
        
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;
