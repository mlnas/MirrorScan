# MirrorScan - AI Model Security Scanner

MirrorScan is a web application that helps you test your AI models for various security vulnerabilities, including:
- Model Inversion Attacks
- PII Leakage
- Embedding Re-identification
- Prompt Artifacts & Memory Residue
- Jailbreak Susceptibility

## Features

- User authentication and authorization
- Create and manage model security scans
- Real-time scan status updates
- Detailed vulnerability reports
- Risk score calculation
- Modern, responsive UI

## Tech Stack

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- SQLite database
- JWT authentication
- Async model scanning

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- React Hooks
- JWT authentication

## Setup

### Backend Setup

1. Create a Python virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python scripts/init_db.py
```

4. Start the backend server:
```bash
uvicorn app.main:app --reload
```

The backend API will be available at http://localhost:8000

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Initial Login

Use these credentials for the first login:
- Email: admin@mirrorscan.ai
- Password: admin123

**Important:** Change these credentials in production!

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Backend Structure
- `app/`: Main application package
  - `api/`: API endpoints
  - `core/`: Core functionality
  - `crud/`: Database operations
  - `models/`: SQLAlchemy models
  - `schemas/`: Pydantic schemas
  - `services/`: Business logic

### Frontend Structure
- `app/`: Next.js app directory
  - `dashboard/`: Dashboard pages
  - `login/`: Authentication pages
- `src/`: Source code
  - `components/`: React components
  - `lib/`: Utilities and hooks

## Security Considerations

1. Change the default superuser credentials
2. Update the SECRET_KEY in production
3. Configure proper CORS settings
4. Use HTTPS in production
5. Implement rate limiting
6. Add proper error logging
7. Regular security audits

## License

MIT License 