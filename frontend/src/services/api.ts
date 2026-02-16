import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  sendOTP: (phoneNumber: string) =>
    api.post('/auth/send-otp', { phone_number: phoneNumber }),
  
  verifyOTP: (phoneNumber: string, otp: string, userData?: any) =>
    api.post('/auth/verify-otp', {
      phone_number: phoneNumber,
      otp: otp,
      ...userData
    }),
  
  register: (userData: any) =>
    api.post('/auth/register', userData),
  
  getCurrentUser: () =>
    api.get('/users/me').then(res => res.data),
  
  refreshToken: () =>
    api.post('/auth/refresh-token'),
  
  logout: () =>
    api.post('/auth/logout'),
};

// Chatbot API
export const chatbotAPI = {
  sendMessage: (message: { content: string; language: string }) =>
    api.post('/chatbot/chat', message).then(res => res.data),
  
  sendVoiceMessage: (message: { transcribed_text: string; language: string }) =>
    api.post('/chatbot/voice-chat', message).then(res => res.data),
  
  getChatHistory: () =>
    api.get('/chatbot/chat-history').then(res => res.data.advisories),
};

// Image Analysis API
export const imageAPI = {
  classifyCropDisease: (formData: FormData, cropType?: string) =>
    api.post('/image/classify-crop-disease', formData, {
      params: { crop_type: cropType },
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(res => res.data),
  
  classifyPest: (formData: FormData, cropType?: string) =>
    api.post('/image/classify-pest', formData, {
      params: { crop_type: cropType },
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(res => res.data),
  
  classifyCrop: (formData: FormData) =>
    api.post('/image/classify-crop', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(res => res.data),
  
  analyzePlantHealth: (formData: FormData, cropType?: string) =>
    api.post('/image/analyze-plant-health', formData, {
      params: { crop_type: cropType },
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(res => res.data),
};

// Market API
export const marketAPI = {
  getPrices: (params?: any) =>
    api.get('/market/prices', { params }).then(res => res.data),
  
  getPriceHistory: (cropName: string, days: number = 30) =>
    api.get(`/market/price-history/${cropName}`, {
      params: { days }
    }).then(res => res.data),
  
  getMarketInsights: () =>
    api.get('/market/insights').then(res => res.data),
  
  setPriceAlert: (alertData: any) =>
    api.post('/market/price-alerts', alertData).then(res => res.data),
};

// Community API
export const communityAPI = {
  getPosts: (params?: any) =>
    api.get('/community/posts', { params }).then(res => res.data),
  
  createPost: (postData: any) =>
    api.post('/community/posts', postData).then(res => res.data),
  
  getPost: (postId: string) =>
    api.get(`/community/posts/${postId}`).then(res => res.data),
  
  likePost: (postId: string) =>
    api.post(`/community/posts/${postId}/like`).then(res => res.data),
  
  commentOnPost: (postId: string, comment: string) =>
    api.post(`/community/posts/${postId}/comments`, { content: comment }).then(res => res.data),
};

// Notifications API
export const notificationAPI = {
  getNotifications: (params?: any) =>
    api.get('/notifications', { params }).then(res => res.data),
  
  markAsRead: (notificationId: string) =>
    api.patch(`/notifications/${notificationId}/read`).then(res => res.data),
  
  markAllAsRead: () =>
    api.patch('/notifications/mark-all-read').then(res => res.data),
  
  updatePreferences: (preferences: any) =>
    api.patch('/notifications/preferences', preferences).then(res => res.data),
};

// User API
export const userAPI = {
  getProfile: () =>
    api.get('/users/me').then(res => res.data),
  
  updateProfile: (userData: any) =>
    api.patch('/users/me', userData).then(res => res.data),
  
  uploadAvatar: (formData: FormData) =>
    api.post('/users/me/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(res => res.data),
};

// Weather API
export const weatherAPI = {
  getCurrentWeather: (location: string) =>
    api.get('/weather/current', { params: { location } }).then(res => res.data),
  
  getWeatherForecast: (location: string, days: number = 7) =>
    api.get('/weather/forecast', { 
      params: { location, days } 
    }).then(res => res.data),
  
  getWeatherAlerts: (location: string) =>
    api.get('/weather/alerts', { params: { location } }).then(res => res.data),
};

// Crop API
export const cropAPI = {
  getCrops: (params?: any) =>
    api.get('/crops', { params }).then(res => res.data),
  
  getCropRecommendations: (params: any) =>
    api.post('/crops/recommendations', params).then(res => res.data),
  
  getCropDetails: (cropId: string) =>
    api.get(`/crops/${cropId}`).then(res => res.data),
};

// Soil API
export const soilAPI = {
  getSoilTypes: () =>
    api.get('/soil/types').then(res => res.data),
  
  addSoilTest: (testData: any) =>
    api.post('/soil/tests', testData).then(res => res.data),
  
  getSoilTests: () =>
    api.get('/soil/tests').then(res => res.data),
};

// Shop API
export const shopAPI = {
  getShops: (params?: any) =>
    api.get('/shops', { params }).then(res => res.data),
  
  getShopInventory: (shopId: string) =>
    api.get(`/shops/${shopId}/inventory`).then(res => res.data),
  
  searchProducts: (query: string) =>
    api.get('/shops/search-products', { params: { q: query } }).then(res => res.data),
};

export default api;
