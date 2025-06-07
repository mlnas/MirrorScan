from typing import List, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
import time

from app.schemas.scan import ScanCreate, Scan, ScanUpdate, ScanRequest, ScanResponse, ScanResult, Vulnerability
from app.models.scan import ScanStatus
from app.db.session import get_db
from app.crud import scan as scan_crud
from app.services.scanner import AIModelScanner, ModelScanner
from app.core.config import settings
from app.core.deps import get_db
from app.services.memory_scanner import MemoryScanner
from app.services.embedding_scanner import EmbeddingScanner
from app.services.redteam_agent import RedTeamAgent
from app.services.guardrails import GuardrailsEngine
from app.services.fingerprinting import ModelFingerprinter
from app.services.forensics import ForensicLogger

router = APIRouter()
model_scanner = ModelScanner()

# Initialize services
memory_scanner = MemoryScanner()
embedding_scanner = EmbeddingScanner()
redteam_agent = RedTeamAgent()
guardrails = GuardrailsEngine()
fingerprinter = ModelFingerprinter()

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
        scan_id = model_scanner.start_scan(
            model_url=scan_request.model_url
        )
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
async def get_security_metrics():
    """
    Get overall security metrics
    """
    try:
        return model_scanner.get_security_metrics()
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

@router.post("/memory", response_model=Scan)
def scan_memory(
    *,
    db: Session = Depends(get_db),
    scan_in: ScanCreate,
    request: Request
) -> dict:
    """
    Scan for model hallucinations and memory traces
    """
    start_time = time.time()
    
    if not scan_in.input_text:
        raise HTTPException(status_code=400, detail="Input text is required")
        
    # Run memory scan
    results = memory_scanner.scan(
        input_text=scan_in.input_text,
        output_text=scan_in.input_text  # In production, this would be model output
    )
    
    # Log scan
    logger = ForensicLogger(db)
    scan_data = {
        "scan_type": "memory",
        "model_name": scan_in.model_name,
        "input_text": scan_in.input_text,
        "threat_level": results["threat_level"],
        "findings": results,
        "memory_traces": results.get("memory_traces"),
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "runtime_ms": int((time.time() - start_time) * 1000)
    }
    logger.log_scan(scan_data)
    
    return scan_data

@router.post("/embedding", response_model=Scan)
def scan_embedding(
    *,
    db: Session = Depends(get_db),
    scan_in: ScanCreate,
    request: Request
) -> dict:
    """
    Scan embeddings for PII and identity leakage
    """
    start_time = time.time()
    
    if not scan_in.input_embeddings:
        raise HTTPException(status_code=400, detail="Input embeddings are required")
        
    # Run embedding scan
    results = embedding_scanner.scan(embeddings=scan_in.input_embeddings)
    
    # Log scan
    logger = ForensicLogger(db)
    scan_data = {
        "scan_type": "embedding",
        "model_name": scan_in.model_name,
        "input_embeddings": scan_in.input_embeddings,
        "threat_level": results["threat_level"],
        "findings": results,
        "pii_detected": results["pii_analysis"],
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "runtime_ms": int((time.time() - start_time) * 1000)
    }
    logger.log_scan(scan_data)
    
    return scan_data

@router.post("/redteam", response_model=Scan)
def run_redteam(
    *,
    db: Session = Depends(get_db),
    scan_in: ScanCreate,
    request: Request
) -> dict:
    """
    Run red team attacks against a model
    """
    start_time = time.time()
    
    # Run attack sequence
    results = redteam_agent.run_attack_sequence(
        target_model_name=scan_in.model_name
    )
    
    # Log scan
    logger = ForensicLogger(db)
    scan_data = {
        "scan_type": "redteam",
        "model_name": scan_in.model_name,
        "threat_level": results["threat_level"],
        "findings": results,
        "attack_vectors": results["attack_results"],
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "runtime_ms": int((time.time() - start_time) * 1000)
    }
    logger.log_scan(scan_data)
    
    return scan_data

@router.post("/protect", response_model=Scan)
def protect_model(
    *,
    db: Session = Depends(get_db),
    scan_in: ScanCreate,
    request: Request
) -> dict:
    """
    Apply runtime protection to model I/O
    """
    start_time = time.time()
    
    if not scan_in.input_text:
        raise HTTPException(status_code=400, detail="Input text is required")
        
    # Apply protection
    results = guardrails.protect(
        input_text=scan_in.input_text,
        output_text=scan_in.input_text,  # In production, this would be model output
        embeddings=scan_in.input_embeddings
    )
    
    # Log scan
    logger = ForensicLogger(db)
    scan_data = {
        "scan_type": "protect",
        "model_name": scan_in.model_name,
        "input_text": scan_in.input_text,
        "threat_level": results["threat_level"],
        "findings": results,
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "runtime_ms": int((time.time() - start_time) * 1000)
    }
    logger.log_scan(scan_data)
    
    return scan_data

@router.post("/fingerprint", response_model=Scan)
def fingerprint_model(
    *,
    db: Session = Depends(get_db),
    scan_in: ScanCreate,
    request: Request
) -> dict:
    """
    Generate model fingerprint and check for drift
    """
    start_time = time.time()
    
    if not scan_in.input_text:
        raise HTTPException(status_code=400, detail="Sample texts are required")
        
    # Generate fingerprint
    texts = [scan_in.input_text]  # In production, this would be multiple samples
    fingerprint = fingerprinter.generate_fingerprint(texts)
    
    # Log scan
    logger = ForensicLogger(db)
    scan_data = {
        "scan_type": "fingerprint",
        "model_name": scan_in.model_name,
        "input_text": scan_in.input_text,
        "findings": fingerprint,
        "model_fingerprint": fingerprint,
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "runtime_ms": int((time.time() - start_time) * 1000)
    }
    logger.log_scan(scan_data)
    
    return scan_data

@router.get("/history", response_model=List[Scan])
def get_scan_history(
    *,
    db: Session = Depends(get_db),
    model_name: Optional[str] = None,
    scan_type: Optional[str] = None,
    min_threat_level: Optional[float] = None,
    limit: int = 100
) -> List[dict]:
    """
    Get scan history with optional filters
    """
    logger = ForensicLogger(db)
    return logger.get_scan_history(
        model_name=model_name,
        scan_type=scan_type,
        min_threat_level=min_threat_level,
        limit=limit
    )

@router.get("/stats/{model_name}", response_model=dict)
def get_model_stats(
    model_name: str,
    db: Session = Depends(get_db)
) -> dict:
    """
    Get statistics for a specific model
    """
    logger = ForensicLogger(db)
    return logger.get_model_stats(model_name) 