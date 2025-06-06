# MirrorScan Backend

FastAPI-based backend for the MirrorScan AI Model Security Scanner.

## Features

- Model vulnerability scanning
- Real-time scan progress monitoring
- Comprehensive security metrics
- Async scan processing
- Rate limiting and security middleware
- Swagger documentation (in development mode)

## API Endpoints

### Scan Operations
- `POST /api/v1/scans/analyze` - Start a new model scan
- `GET /api/v1/scans/status/{scan_id}` - Get scan status
- `GET /api/v1/scans/vulnerabilities` - List detected vulnerabilities
- `GET /api/v1/scans/metrics` - Get security metrics
- `POST /api/v1/scans/containment/{scan_id}` - Initiate containment protocols

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `GET /api/v1/auth/me` - Get current user info

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```env
PROJECT_NAME=MirrorScan
VERSION=0.1.0
ENVIRONMENT=development
SECRET_KEY=your-secret-key
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
DATABASE_URL=postgresql://user:password@localhost:5432/mirrorscan
RATE_LIMIT_PER_MINUTE=60
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

## Development

The API will be available at `http://localhost:8000`

- API documentation (development only):
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`

## Testing

Run tests with pytest:
```bash
pytest
```

## Security Features

- Rate limiting
- CORS protection
- Session middleware
- Trusted host validation
- Gzip compression
- Security headers
- Input validation
- Authentication required for all scan endpoints

## Scan Types

The scanner checks for various vulnerabilities:
- Model inversion attacks
- PII leakage
- Embedding re-identification
- Prompt artifacts & memory residue
- Jailbreak susceptibility
- Self-modification vulnerabilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 