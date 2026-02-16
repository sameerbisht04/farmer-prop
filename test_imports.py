#!/usr/bin/env python3
"""
Test script to check for import errors in the Smart Crop Advisory System
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test all critical imports"""
    errors = []
    
    try:
        from app.core.config import settings
        print("✅ Config import successful")
    except Exception as e:
        errors.append(f"Config import failed: {e}")
        print(f"❌ Config import failed: {e}")
    
    try:
        from app.core.database import engine, Base
        print("✅ Database import successful")
    except Exception as e:
        errors.append(f"Database import failed: {e}")
        print(f"❌ Database import failed: {e}")
    
    try:
        from app.models.user import User
        print("✅ User model import successful")
    except Exception as e:
        errors.append(f"User model import failed: {e}")
        print(f"❌ User model import failed: {e}")
    
    try:
        from app.api.api_v1.api import api_router
        print("✅ API router import successful")
    except Exception as e:
        errors.append(f"API router import failed: {e}")
        print(f"❌ API router import failed: {e}")
    
    try:
        from app.services.chatbot_service import ChatbotService
        print("✅ Chatbot service import successful")
    except Exception as e:
        errors.append(f"Chatbot service import failed: {e}")
        print(f"❌ Chatbot service import failed: {e}")
    
    try:
        from app.services.image_classification_service import ImageClassificationService
        print("✅ Image classification service import successful")
    except Exception as e:
        errors.append(f"Image classification service import failed: {e}")
        print(f"❌ Image classification service import failed: {e}")
    
    if errors:
        print(f"\n❌ Found {len(errors)} import errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

if __name__ == "__main__":
    print("🧪 Testing Smart Crop Advisory System imports...")
    print("=" * 50)
    
    success = test_imports()
    
    if success:
        print("\n🎉 All imports are working correctly!")
        print("The system is ready to run (once dependencies are installed).")
    else:
        print("\n⚠️  Some imports failed. Please check the errors above.")
        print("Make sure all dependencies are installed and files are in the correct locations.")
    
    sys.exit(0 if success else 1)
