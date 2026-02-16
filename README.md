# Smart Crop Advisory System

An AI-powered advisory system designed specifically for small and marginal farmers in India, providing personalized crop recommendations, pest identification, and farming guidance in multiple languages.

## 🌾 Features

- **Multilingual AI Chatbot** (Hindi, English, Punjabi)
- **Voice Assistance** for low-literate farmers
- **Image Classification** for crop/pest disease identification
- **Smart Notifications** via SMS/WhatsApp
- **Community Platform** for farmer interaction
- **Government Shop Integration** for input tracking
- **Market Insights** with real-time price tracking
- **Continuous Learning** with AI feedback improvement

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite works for development)
- Redis (optional, for caching)

### Automated Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-crop-advisory
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Start development servers**
   ```bash
   python run_dev.py
   ```

### Manual Setup

1. **Install dependencies**
   ```bash
   npm run install-all
   ```

2. **Set up environment variables**
   ```bash
   cp env.example backend/.env
   # Edit backend/.env with your configuration
   ```

3. **Set up database**
   ```bash
   cd backend
   python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
   ```

4. **Run the application**
   ```bash
   npm run dev
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Docker Setup (Production)

```bash
docker-compose up -d
```

## 🏗️ Architecture

```
smart-crop-advisory/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── alembic/            # Database migrations
│   └── main.py             # FastAPI application
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Frontend utilities
│   └── public/             # Static assets
├── models/                 # AI/ML models
├── data/                   # Training data and datasets
└── docs/                   # Documentation
```

## 🌍 Supported Languages

- Hindi (हिंदी)
- English
- Punjabi (ਪੰਜਾਬੀ)

## 🤖 AI Features

- **Crop Recommendation Engine**: Analyzes soil type, weather, and market conditions
- **Disease Identification**: Computer vision for pest and disease detection
- **Natural Language Processing**: Multilingual chatbot with agricultural knowledge
- **Predictive Analytics**: Weather-based farming recommendations

## 📱 Mobile Support

The system is designed to work seamlessly on mobile devices, with special consideration for:
- Low-bandwidth connections
- Touch-friendly interface
- Offline capability for basic features

## 🔧 Configuration

Key configuration options in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/smart_crop_advisory

# AI Services
OPENAI_API_KEY=your_openai_key
GOOGLE_TRANSLATE_API_KEY=your_google_key

# Notifications
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token

# Weather API
OPENWEATHER_API_KEY=your_openweather_key
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Indian Council of Agricultural Research (ICAR)
- Local farming communities and agricultural experts
- Open source AI/ML libraries and frameworks

## 📞 Support

For support and questions:
- GitHub Issues: [Create an issue](https://github.com/your-repo/issues)
- Email: support@smartcropadvisory.com
- Documentation: [Full Documentation](docs/)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📊 Project Status

- ✅ **Core Features**: AI Chatbot, Image Classification, Voice Assistance
- ✅ **Backend**: FastAPI with comprehensive API endpoints
- ✅ **Frontend**: React with multilingual support
- ✅ **Database**: Complete schema design
- ✅ **Deployment**: Docker configuration ready
- 🚧 **In Progress**: Community Platform, Market Insights, Shop Integration
- 📋 **Planned**: Mobile App, Advanced Analytics, IoT Integration

## 🎯 Impact Goals

- **Target Users**: 10,000+ small and marginal farmers
- **Languages**: Hindi, English, Punjabi (expandable)
- **Coverage**: All major agricultural regions in India
- **Accuracy**: >85% disease/pest identification accuracy
- **Response Time**: <3 seconds for AI recommendations
