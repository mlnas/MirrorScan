from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.scan import ModelScan, Vulnerability
from app.schemas.scan import ScanCreate, ScanUpdate

def get_scan(db: Session, scan_id: int) -> Optional[ModelScan]:
    """Get a scan by ID"""
    return db.query(ModelScan).filter(ModelScan.id == scan_id).first()

def get_scans(db: Session, skip: int = 0, limit: int = 100) -> List[ModelScan]:
    """Get all scans with pagination"""
    return db.query(ModelScan).offset(skip).limit(limit).all()

def create_scan(db: Session, obj_in: ScanCreate) -> ModelScan:
    """Create a new scan"""
    db_obj = ModelScan(
        model_name=obj_in.model_name,
        model_type=obj_in.model_type,
        api_endpoint=obj_in.api_endpoint
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_scan(db: Session, db_obj: ModelScan, obj_in: ScanUpdate) -> ModelScan:
    """Update a scan"""
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_scan(db: Session, scan_id: int) -> bool:
    """Delete a scan"""
    scan = db.query(ModelScan).filter(ModelScan.id == scan_id).first()
    if scan:
        db.delete(scan)
        db.commit()
        return True
    return False

def add_vulnerability(
    db: Session,
    scan_id: int,
    vulnerability_type: str,
    severity: float,
    description: str,
    evidence: str,
    remediation: str
) -> Vulnerability:
    """Add a vulnerability to a scan"""
    vuln = Vulnerability(
        scan_id=scan_id,
        vulnerability_type=vulnerability_type,
        severity=severity,
        description=description,
        evidence=evidence,
        remediation=remediation
    )
    db.add(vuln)
    db.commit()
    db.refresh(vuln)
    return vuln 