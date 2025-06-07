from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    MirrorScan - AI Model Security Scanner
    
    Test your AI models for:
    * Model Inversion Attacks
    * PII Leakage
    * Embedding Re-identification
    * Prompt Artifacts & Memory Residue
    * Jailbreak Susceptibility
    """,
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/")
def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "message": "Welcome to MirrorScan API",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 