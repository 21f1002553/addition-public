cat > README.md << 'EOF'
# HR Management System - Backend

Complete backend API for HR Management System with AI-powered features.

##  Features

### Core Modules
- **User Management** - User accounts and roles
- **Job Management** - Job postings and applications
- **Expense Management**  - Complete expense tracking with AI

### Expense Management API
-  11 REST API endpoints
-  AI-powered receipt verification
-  Approval/rejection workflow
-  Policy compliance checking
-  Analytics and reporting
-  File upload support (PDF, images)
-  Comprehensive test suite

## 📋 API Endpoints

### Expenses
- `POST /api/expenses/submit` - Submit expense
- `GET /api/expenses/` - Get all expenses
- `GET /api/expenses/{id}` - Get single expense
- `PUT /api/expenses/{id}/approve` - Approve expense
- `PUT /api/expenses/{id}/reject` - Reject expense
- `GET /api/expenses/pending` - Get pending expenses
- `GET /api/expenses/reports` - Get analytics



##  Tech Stack

- **Framework**: Flask 2.3.3
- **Database**: SQLAlchemy with SQLite/PostgreSQL
- **AI/ML**: Google Gemini, OpenAI GPT
- **Vector DB**: ChromaDB
- **Testing**: Pytest



### Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/SE_SEP_Team18_Backend.git
cd SE_SEP_Team18_Backend

# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start server
python run.py
```

### Testing
```bash
# Run all tests
pytest tests/test_expense_api.py -v

# Test API manually
curl http://localhost:5001/health
```

## Project Structure
```
backend/
├── app.py                    # Flask application
├── run.py                    # Server entry point
├── init_db.py               # Database initialization
├── models.py                # Database models
├── routes/
│   ├── expense_routes.py    # Expense API endpoints
│   ├── user_routes.py       # User management
│   └── role_routes.py       # Role management
├── genai/
│   └── services/
│       └── expense_service.py  # AI services
└── tests/
    └── test_expense_api.py  # API tests
```

## Environment Variables

Create a `.env` file:
```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///hr_system.db
GEMINI_API_KEY=your-gemini-key
OPENAI_API_KEY=your-openai-key
```



