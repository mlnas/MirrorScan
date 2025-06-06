from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
import enum

from app.db.base_class import Base

class ScanStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class VulnerabilityType(str, enum.Enum):
    MODEL_INVERSION = "model_inversion"
    PII_LEAKAGE = "pii_leakage"
    EMBEDDING_REIDENTIFICATION = "embedding_reidentification"
    PROMPT_ARTIFACTS = "prompt_artifacts"
    JAILBREAK = "jailbreak"

class ModelScan(Base):
    """Model for storing AI model scan results"""
    __tablename__ = "model_scans"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    model_type = Column(String)
    api_endpoint = Column(String)
    status = Column(String, default=ScanStatus.PENDING)
    risk_score = Column(Float, default=0.0)
    scan_results = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Vulnerability(Base):
    """Model for storing individual vulnerabilities found in a scan"""
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("model_scans.id"))
    vulnerability_type = Column(String)
    severity = Column(Float)
    description = Column(String)
    evidence = Column(String)
    remediation = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 