from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum

class ScanStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CONTAINED = "contained"

class VulnerabilityType(str, Enum):
    MODEL_INVERSION = "model_inversion"
    PII_LEAKAGE = "pii_leakage"
    EMBEDDING_LEAKAGE = "embedding_leakage"
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"

class VulnerabilitySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ScanRequest(BaseModel):
    model_url: str
    scan_mode: Optional[str] = "comprehensive"

class ScanResponse(BaseModel):
    scan_id: str
    status: str
    message: str

class Vulnerability(BaseModel):
    type: str
    severity: VulnerabilitySeverity
    description: str
    detection_time: str
    details: Dict[str, Any]
    mitigation_steps: List[str]

class ScanResult(BaseModel):
    scan_id: str
    status: str
    progress: float
    vulnerabilities: List[Dict[str, Any]]
    security_score: float
    start_time: str
    end_time: Optional[str] = None
    model_url: str
    headers: Dict[str, str] = {}
    error_message: Optional[str] = None

    @validator("security_score")
    def validate_security_score(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Security score must be between 0 and 100")
        return v

    @validator("progress")
    def validate_progress(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Progress must be between 0 and 100")
        return v

class VulnerabilityBase(BaseModel):
    vulnerability_type: VulnerabilityType
    severity: float
    description: str
    evidence: Dict[str, Any]
    remediation: str

class VulnerabilityCreate(VulnerabilityBase):
    pass

class Vulnerability(VulnerabilityBase):
    id: int
    scan_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ScanBase(BaseModel):
    model_name: str = Field(..., description="Name/identifier of the model being scanned")
    scan_type: str = Field(..., description="Type of scan to perform")

class ScanCreate(ScanBase):
    input_text: Optional[str] = Field(None, description="Input text for memory/redteam scans")
    input_embeddings: Optional[List[List[float]]] = Field(None, description="Input embeddings for embedding scans")

class ScanUpdate(BaseModel):
    status: Optional[str] = None
    completed_at: Optional[datetime] = None
    threat_level: Optional[float] = None
    findings: Optional[Dict] = None
    memory_traces: Optional[Dict] = None
    pii_detected: Optional[Dict] = None
    attack_vectors: Optional[Dict] = None
    model_fingerprint: Optional[Dict] = None
    error_message: Optional[str] = None

class ScanInDBBase(ScanBase):
    id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    threat_level: Optional[float] = None
    findings: Optional[Dict] = None
    memory_traces: Optional[Dict] = None
    pii_detected: Optional[Dict] = None
    attack_vectors: Optional[Dict] = None
    model_fingerprint: Optional[Dict] = None
    runtime_ms: Optional[int] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

class Scan(ScanInDBBase):
    pass

class ScanInDB(ScanInDBBase):
    pass

class SecurityMetrics(BaseModel):
    total_vulnerabilities: int
    critical_issues: int
    security_score: float

# Request Validation
class ScanValidation(BaseModel):
    is_valid: bool
    errors: List[str] = [] 