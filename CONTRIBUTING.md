# Contributing to Smart Crop Advisory System

Thank you for your interest in contributing to the Smart Crop Advisory System! This document provides guidelines and information for contributors.

## 🌾 Project Overview

The Smart Crop Advisory System is an AI-powered platform designed to help small and marginal farmers in India make informed decisions about crop selection, pest control, and farming practices.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite works for development)
- Git

### Development Setup

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

## 📁 Project Structure

```
smart-crop-advisory/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── schemas/        # Pydantic schemas
│   ├── alembic/            # Database migrations
│   └── main.py             # FastAPI application
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── contexts/       # React contexts
│   │   └── types/          # TypeScript types
│   └── public/             # Static assets
├── docs/                   # Documentation
└── tests/                  # Test files
```

## 🛠️ Development Guidelines

### Backend Development

1. **Code Style**
   - Follow PEP 8 for Python code
   - Use type hints for all functions
   - Write docstrings for all public functions and classes

2. **Database Changes**
   - Create migrations using Alembic for schema changes
   - Test migrations on a copy of production data

3. **API Design**
   - Follow RESTful conventions
   - Use appropriate HTTP status codes
   - Include proper error handling and validation

4. **Testing**
   - Write unit tests for all new functionality
   - Use pytest for testing
   - Aim for >80% code coverage

### Frontend Development

1. **Code Style**
   - Use TypeScript for all new components
   - Follow React best practices
   - Use functional components with hooks

2. **Styling**
   - Use Tailwind CSS for styling
   - Follow mobile-first design principles
   - Ensure accessibility compliance

3. **State Management**
   - Use React Query for server state
   - Use React Context for global client state
   - Keep component state local when possible

## 🌍 Internationalization

The system supports multiple languages (Hindi, English, Punjabi). When adding new text:

1. Add translations to `frontend/src/i18n.ts`
2. Use the `t()` function for all user-facing text
3. Test in all supported languages

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Integration Testing
```bash
# Run full test suite
python -m pytest tests/integration/ -v
```

## 📝 Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   - Run the test suite
   - Test manually in different browsers
   - Test with different languages

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**
   - Operating system
   - Browser version (for frontend issues)
   - Python/Node.js versions

2. **Steps to reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior

3. **Additional context**
   - Screenshots or error messages
   - Relevant log files

## 💡 Feature Requests

When suggesting new features:

1. **Check existing issues** to avoid duplicates
2. **Provide clear use cases** and benefits
3. **Consider implementation complexity**
4. **Think about user experience** for farmers

## 🏗️ Architecture Decisions

### Technology Choices

- **Backend**: FastAPI for high performance and automatic API documentation
- **Frontend**: React with TypeScript for type safety and modern development
- **Database**: PostgreSQL for production, SQLite for development
- **AI/ML**: PyTorch for image classification, Transformers for NLP
- **Notifications**: Twilio for SMS, WhatsApp Business API

### Design Principles

1. **Accessibility First**: Ensure the system works for users with varying technical literacy
2. **Mobile-First**: Most farmers use mobile devices
3. **Offline Capability**: Basic features should work without internet
4. **Multilingual**: Support for local languages is essential
5. **Privacy**: Protect farmer data and provide transparency

## 📊 Performance Guidelines

### Backend Performance
- Use database indexes for frequently queried fields
- Implement caching for expensive operations
- Use async/await for I/O operations
- Monitor API response times

### Frontend Performance
- Lazy load components and routes
- Optimize images and assets
- Use React.memo for expensive components
- Implement proper error boundaries

## 🔒 Security Guidelines

1. **Authentication**: Use JWT tokens with proper expiration
2. **Authorization**: Implement role-based access control
3. **Input Validation**: Validate all user inputs
4. **Data Protection**: Encrypt sensitive data
5. **API Security**: Use rate limiting and CORS properly

## 📚 Documentation

### Code Documentation
- Write clear docstrings for all functions
- Include type hints for better IDE support
- Document complex algorithms and business logic

### User Documentation
- Keep README.md updated
- Write clear API documentation
- Provide user guides for farmers

## 🤝 Community Guidelines

1. **Be respectful** and inclusive
2. **Help others** learn and contribute
3. **Provide constructive feedback**
4. **Follow the code of conduct**

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For security issues or private matters

## 🎯 Roadmap

### Short Term (Next 3 months)
- [ ] Complete community platform features
- [ ] Implement market price tracking
- [ ] Add government shop integration
- [ ] Improve AI model accuracy

### Medium Term (3-6 months)
- [ ] Add offline functionality
- [ ] Implement push notifications
- [ ] Add more language support
- [ ] Create mobile app

### Long Term (6+ months)
- [ ] Advanced analytics dashboard
- [ ] Integration with IoT sensors
- [ ] Blockchain for supply chain tracking
- [ ] Machine learning model improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for contributing to the Smart Crop Advisory System! Together, we can help farmers make better decisions and improve agricultural outcomes. 🌾
