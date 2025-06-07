# MirrorScan - AI Model Security Scanner

MirrorScan is an advanced security scanning and monitoring platform for AI models. It provides real-time forensic scanning, autonomous red teaming, and runtime guardrails for deployed GenAI models.

## Features

- 🧠 **Model Memory & Hallucination Scanner**: Detects rare, out-of-distribution, or training data-like content in model responses
- 🔍 **Embedding Re-identification Engine**: Identifies potential PII and identity leakage in model embeddings
- 🛠️ **Autonomous Red Team Agent**: Automatically tests models against prompt injection, jailbreaks, and data extraction attempts
- 🔐 **Runtime Guardrails**: Provides real-time protection against PII exposure, toxic content, and hallucinations
- 📦 **Model Drift & Fingerprinting**: Tracks model behavior changes and generates unique behavioral signatures
- 🧾 **AI Forensic Logging**: Comprehensive logging of all model interactions with powerful filtering capabilities

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Redis
- **Frontend**: Next.js 14, React 18, Tailwind CSS
- **AI/ML**: PyTorch, Transformers, Sentence Transformers
- **Database**: PostgreSQL
- **Infrastructure**: Docker, Nginx

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mirrorscan.git
   cd mirrorscan
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Create environment files:
   ```bash
   # backend/.env
   DATABASE_URL=postgresql://mirrorscan:changeme@localhost:5432/mirrorscan
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your-secret-key
   
   # frontend/.env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

5. Initialize the database:
   ```bash
   cd backend
   alembic upgrade head
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Or use Docker Compose to start everything:
   ```bash
   docker-compose up -d
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Usage

### Scanning a Model

```python
import requests

# Memory Scanner
response = requests.post("http://localhost:8000/api/v1/scans/memory", json={
    "model_name": "gpt-4",
    "scan_type": "memory",
    "input_text": "Your test prompt here"
})

# Embedding Scanner
response = requests.post("http://localhost:8000/api/v1/scans/embedding", json={
    "model_name": "text-embedding-3-large",
    "scan_type": "embedding",
    "input_embeddings": [[0.1, 0.2, ...], [0.3, 0.4, ...]]
})

# Red Team
response = requests.post("http://localhost:8000/api/v1/scans/redteam", json={
    "model_name": "mistral-7b",
    "scan_type": "redteam"
})
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 