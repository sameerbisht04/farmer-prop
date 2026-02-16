# 🚀 Smart Crop Advisory System - Installation Guide

## Quick Start (Recommended)

### Step 1: Install Python Dependencies
```bash
# Install core dependencies
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv

# Install AI/ML dependencies (optional for basic functionality)
pip install torch torchvision transformers opencv-python pillow numpy scikit-learn pandas

# Install additional dependencies (optional)
pip install googletrans langdetect speechrecognition pyttsx3 pydub twilio requests pyowm matplotlib redis
```

### Step 2: Test the Installation
```bash
python test_imports.py
```

### Step 3: Start the Backend
```bash
cd backend
python main.py
```

### Step 4: Start the Frontend (in another terminal)
```bash
cd frontend
npm install
npm start
```

### Step 5: Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Detailed Installation

### Option 1: Automated Setup
```bash
python setup.py
```

### Option 2: Manual Setup

#### Backend Setup
```bash
# Create virtual environment
python -m venv backend/venv

# Activate virtual environment
# Windows:
backend\venv\Scripts\activate
# Linux/Mac:
source backend/venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env.example backend/.env
```

#### Frontend Setup
```bash
cd frontend
npm install
```

### Option 3: Docker Setup
```bash
docker-compose up -d
```

## Troubleshooting

### Common Issues

#### 1. "No module named 'fastapi'"
**Solution**: Install FastAPI
```bash
pip install fastapi uvicorn
```

#### 2. "No module named 'sqlalchemy'"
**Solution**: Install SQLAlchemy
```bash
pip install sqlalchemy
```

#### 3. "No module named 'pydantic_settings'"
**Solution**: Install pydantic-settings
```bash
pip install pydantic-settings
```

#### 4. Import errors in API endpoints
**Solution**: All endpoint files have been created. The import errors should be resolved.

### Verification Steps

1. **Test Imports**:
   ```bash
   python test_imports.py
   ```
   Should show: ✅ All imports successful!

2. **Test Backend**:
   ```bash
   cd backend
   python main.py
   ```
   Should show: Uvicorn running on http://0.0.0.0:8000

3. **Test API**:
   - Open http://localhost:8000
   - Open http://localhost:8000/docs

## Environment Configuration

Create `backend/.env` file:
```env
DATABASE_URL=sqlite:///./smart_crop_advisory.db
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Features Available

Once installed, you'll have access to:

- ✅ **AI Chatbot** - Multilingual crop advisory
- ✅ **Image Analysis** - Disease and pest identification
- ✅ **Voice Assistance** - Speech recognition and synthesis
- ✅ **User Management** - OTP-based authentication
- ✅ **Database** - Complete schema for all features
- ✅ **API Documentation** - Interactive API explorer
- ✅ **Frontend Interface** - Modern React application

## Support

If you encounter any issues:
1. Check the [ERROR_FIXES.md](ERROR_FIXES.md) file
2. Run `python test_imports.py` to identify specific import errors
3. Ensure all dependencies are installed correctly

## Next Steps

After successful installation:
1. Update `backend/.env` with your API keys (optional)
2. Customize the application for your specific needs
3. Deploy to production using Docker or cloud services

---

**🎉 The Smart Crop Advisory System is now ready to help farmers make better agricultural decisions!**
