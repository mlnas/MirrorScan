from typing import Optional, Dict, Any, List
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from app.models.scan import ScanStatus, VulnerabilityType
from enum import Enum

class VulnerabilityType(str, Enum):
    MODEL_INVERSION = "model_inversion"
    PII_LEAKAGE = "pii_leakage"
    EMBEDDING_REIDENTIFICATION = "embedding_reidentification"
    PROMPT_ARTIFACT = "prompt_artifact"
    JAILBREAK = "jailbreak"
    SELF_MODIFICATION = "self_modification"

class VulnerabilitySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ScanStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CONTAINED = "contained"

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
    model_name: str
    model_type: str
    api_endpoint: HttpUrl

class ScanCreate(ScanBase):
    pass

class ScanUpdate(BaseModel):
    status: Optional[ScanStatus] = None
    risk_score: Optional[float] = None
    scan_results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class Scan(ScanBase):
    id: int
    status: ScanStatus
    risk_score: float = 0.0
    scan_results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    vulnerabilities: List[Vulnerability] = []

    class Config:
        from_attributes = True

class ScanRequest(BaseModel):
    model_url: HttpUrl

class ScanResponse(BaseModel):
    scan_id: str
    status: str
    message: str

class ScanResult(BaseModel):
    vulnerabilities: List[Dict[str, Any]]

class SecurityMetrics(BaseModel):
    models_scanned: int
    vulnerabilities_detected: int
    security_score: float
    critical_issues: int
    scan_history: List[dict]

# Request Validation
class ScanValidation(BaseModel):
    is_valid: bool
    errors: List[str] = [] 