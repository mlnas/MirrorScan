from typing import List, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.schemas.scan import ScanCreate, Scan, ScanUpdate, ScanRequest, ScanResponse, ScanResult, Vulnerability
from app.models.scan import ScanStatus
from app.db.session import get_db
from app.crud import scan as scan_crud
from app.services.scanner import AIModelScanner, ModelScanner
from app.core.config import settings

router = APIRouter()
model_scanner = ModelScanner()

async def run_scan(scan_id: int, db: Session):
    """Background task to run the scan"""
    scan = scan_crud.get_scan(db=db, scan_id=scan_id)
    if not scan:
        return
    
    try:
        # Update scan status
        scan = scan_crud.update_scan(
            db=db,
            db_obj=scan,
            obj_in={"status": ScanStatus.IN_PROGRESS}
        )
        
        # Create scanner instance and run scan
        scanner = AIModelScanner(
            api_endpoint=scan.api_endpoint,
            model_type=scan.model_type
        )
        
        vulnerabilities = await scanner.run_full_scan()
        
        # Calculate risk score
        risk_score = sum(v["severity"] for v in vulnerabilities) / len(vulnerabilities) if vulnerabilities else 0.0
        
        # Add vulnerabilities to database
        for vuln in vulnerabilities:
            scan_crud.add_vulnerability(
                db=db,
                scan_id=scan_id,
                vulnerability_type=vuln["vulnerability_type"],
                severity=vuln["severity"],
                description=vuln["description"],
                evidence=vuln["evidence"],
                remediation=vuln["remediation"]
            )
        
        # Update scan with results
        scan_crud.update_scan(
            db=db,
            db_obj=scan,
            obj_in={
                "status": ScanStatus.COMPLETED,
                "risk_score": risk_score,
                "scan_results": {"vulnerabilities": vulnerabilities}
            }
        )
        
    except Exception as e:
        # Update scan status to failed
        scan_crud.update_scan(
            db=db,
            db_obj=scan,
            obj_in={
                "status": ScanStatus.FAILED,
                "error_message": str(e)
            }
        )

@router.post("/", response_model=Scan)
async def create_scan(
    scan_in: ScanCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> Any:
    """
    Create new scan and run it in the background.
    """
    # Create scan record
    scan = scan_crud.create_scan(db=db, obj_in=scan_in)
    
    # Start scan in background
    background_tasks.add_task(run_scan, scan.id, db)
    
    return scan

@router.get("/", response_model=List[Scan])
def list_scans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve scans for current user.
    """
    return scan_crud.get_scans_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{scan_id}", response_model=Scan)
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get scan by ID.
    """
    scan = scan_crud.get_scan(db=db, scan_id=scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return scan

@router.put("/{scan_id}", response_model=Scan)
def update_scan(
    scan_id: int,
    scan_in: ScanUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Update scan.
    """
    scan = scan_crud.get_scan(db=db, scan_id=scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    scan = scan_crud.update_scan(
        db=db,
        db_obj=scan,
        obj_in=scan_in.model_dump(exclude_unset=True)
    )
    return scan

@router.delete("/{scan_id}")
def delete_scan(
    scan_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Delete scan.
    """
    scan = scan_crud.get_scan(db=db, scan_id=scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if not scan_crud.delete_scan(db=db, scan_id=scan_id):
        raise HTTPException(status_code=404, detail="Scan not found")
    return {"ok": True}

@router.post("/analyze", response_model=ScanResponse)
async def analyze_model(
    scan_request: ScanRequest,
    background_tasks: BackgroundTasks,
):
    """
    Analyze an AI model for security vulnerabilities
    """
    try:
        # Start async scan
        scan_id = model_scanner.start_scan(scan_request.model_url)
        background_tasks.add_task(model_scanner.run_analysis, scan_id)
        
        return {
            "scan_id": scan_id,
            "status": "initiated",
            "message": "Model analysis started"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status/{scan_id}", response_model=ScanResult)
async def get_scan_status(
    scan_id: str,
):
    """
    Get the status of a model scan
    """
    try:
        result = model_scanner.get_scan_status(scan_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/vulnerabilities", response_model=List[Vulnerability])
async def get_vulnerabilities(
):
    """
    Get list of detected vulnerabilities
    """
    try:
        return model_scanner.get_vulnerabilities()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_security_metrics(
):
    """
    Get security metrics and statistics
    """
    try:
        return {
            "models_scanned": model_scanner.get_total_scans(),
            "vulnerabilities_detected": model_scanner.get_total_vulnerabilities(),
            "security_score": model_scanner.calculate_security_score(),
            "critical_issues": model_scanner.get_critical_issues_count()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/containment/{scan_id}")
async def initiate_containment(
    scan_id: str,
):
    """
    Initiate containment protocols for compromised model
    """
    try:
        model_scanner.initiate_containment(scan_id)
        return {"status": "success", "message": "Containment protocols initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 