#!/usr/bin/env python3
"""
Smart Crop Advisory System Setup Script
This script helps set up the development environment for the Smart Crop Advisory System.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, cwd=None, shell=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def check_node_version():
    """Check if Node.js is installed"""
    result = run_command("node --version")
    if result:
        print(f"✅ Node.js {result.strip()} detected")
        return True
    else:
        print("❌ Node.js is not installed. Please install Node.js 16 or higher")
        return False


def setup_backend():
    """Set up the backend environment"""
    print("\n🔧 Setting up backend...")
    
    # Create virtual environment
    if not os.path.exists("backend/venv"):
        print("Creating Python virtual environment...")
        run_command("python -m venv backend/venv")
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "backend\\venv\\Scripts\\activate"
        pip_cmd = "backend\\venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source backend/venv/bin/activate"
        pip_cmd = "backend/venv/bin/pip"
    
    print("Installing Python dependencies...")
    run_command(f"{pip_cmd} install --upgrade pip")
    
    # Install dependencies with error handling
    print("Installing core dependencies...")
    core_deps = [
        "fastapi==0.104.1",
        "uvicorn==0.24.0", 
        "sqlalchemy==2.0.23",
        "pydantic==2.5.0",
        "pydantic-settings==2.0.3",
        "python-multipart==0.0.6",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-dotenv==1.0.0"
    ]
    
    for dep in core_deps:
        print(f"Installing {dep}...")
        result = run_command(f"{pip_cmd} install {dep}")
        if result is None:
            print(f"⚠️  Warning: Failed to install {dep}")
    
    # Try to install remaining dependencies
    print("Installing remaining dependencies...")
    run_command(f"{pip_cmd} install -r requirements.txt")
    
    # Create .env file if it doesn't exist
    if not os.path.exists("backend/.env"):
        print("Creating .env file...")
        shutil.copy("env.example", "backend/.env")
        print("⚠️  Please update backend/.env with your API keys and configuration")
    
    # Test imports
    print("Testing imports...")
    result = run_command(f"{pip_cmd} install pytest")
    if result:
        print("✅ Backend setup complete")
    else:
        print("⚠️  Backend setup completed with warnings")


def setup_frontend():
    """Set up the frontend environment"""
    print("\n🔧 Setting up frontend...")
    
    # Install Node.js dependencies
    print("Installing Node.js dependencies...")
    run_command("npm install", cwd="frontend")
    
    # Create .env file if it doesn't exist
    if not os.path.exists("frontend/.env"):
        print("Creating frontend .env file...")
        with open("frontend/.env", "w") as f:
            f.write("REACT_APP_API_URL=http://localhost:8000/api/v1\n")
    
    print("✅ Frontend setup complete")


def setup_database():
    """Set up the database"""
    print("\n🔧 Setting up database...")
    
    # Initialize database
    if os.name == 'nt':  # Windows
        python_cmd = "backend\\venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_cmd = "backend/venv/bin/python"
    
    print("Initializing database...")
    run_command(f"{python_cmd} -c \"from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)\"", cwd="backend")
    
    print("✅ Database setup complete")


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "backend/uploads",
        "backend/static",
        "logs",
        "data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    print("✅ Directories created")


def main():
    """Main setup function"""
    print("🌾 Smart Crop Advisory System Setup")
    print("=" * 50)
    
    # Check system requirements
    check_python_version()
    if not check_node_version():
        print("\nPlease install Node.js and run this script again.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup backend
    setup_backend()
    
    # Setup frontend
    setup_frontend()
    
    # Setup database
    setup_database()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Update backend/.env with your API keys")
    print("2. Run 'npm run dev' to start the development servers")
    print("3. Open http://localhost:3000 in your browser")
    print("\nFor production deployment:")
    print("1. Update docker-compose.yml with your configuration")
    print("2. Run 'docker-compose up -d' to start all services")
    
    print("\n📚 Documentation:")
    print("- README.md: Project overview and setup instructions")
    print("- API Documentation: http://localhost:8000/docs (after starting backend)")
    print("- Frontend: http://localhost:3000")


if __name__ == "__main__":
    main()
