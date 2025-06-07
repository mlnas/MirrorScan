from datetime import datetime
from typing import Dict, List, Optional
import enum
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Scan(Base):
    id = Column(Integer, primary_key=True, index=True)
    scan_type = Column(String, nullable=False)  # memory, embedding, redteam, etc.
    status = Column(String, nullable=False)  # running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Input data
    model_name = Column(String, nullable=False)
    input_text = Column(String, nullable=True)
    input_embeddings = Column(JSON, nullable=True)  # For embedding scans
    
    # Results
    threat_level = Column(Float, nullable=True)  # 0-1 score
    findings = Column(JSON, nullable=True)  # Detailed scan results
    memory_traces = Column(JSON, nullable=True)  # For memory scans
    pii_detected = Column(JSON, nullable=True)  # For PII scans
    attack_vectors = Column(JSON, nullable=True)  # For red team scans
    model_fingerprint = Column(JSON, nullable=True)  # For fingerprinting
    
    # Metadata
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    runtime_ms = Column(Integer, nullable=True)
    error_message = Column(String, nullable=True)

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