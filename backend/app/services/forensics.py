from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging
from sqlalchemy.orm import Session
from app.models.scan import Scan
from app.core.config import settings

class ForensicLogger:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger("forensics")
        
    def _sanitize_for_logging(self, data: Any) -> Any:
        """Sanitize sensitive data before logging"""
        if isinstance(data, dict):
            return {k: self._sanitize_for_logging(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_for_logging(v) for v in data]
        elif isinstance(data, str):
            # Basic PII patterns to redact
            patterns = {
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b': '[REDACTED EMAIL]',
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b': '[REDACTED PHONE]',
                r'\b\d{3}-\d{2}-\d{4}\b': '[REDACTED SSN]'
            }
            result = data
            for pattern, replacement in patterns.items():
                result = re.sub(pattern, replacement, result)
            return result
        return data
        
    def log_scan(self, scan_data: Dict) -> None:
        """Log a model scan event"""
        try:
            # Create scan record
            scan = Scan(
                scan_type=scan_data["scan_type"],
                status="completed",
                model_name=scan_data["model_name"],
                input_text=scan_data.get("input_text"),
                input_embeddings=scan_data.get("input_embeddings"),
                threat_level=scan_data.get("threat_level"),
                findings=scan_data.get("findings"),
                memory_traces=scan_data.get("memory_traces"),
                pii_detected=scan_data.get("pii_detected"),
                attack_vectors=scan_data.get("attack_vectors"),
                model_fingerprint=scan_data.get("model_fingerprint"),
                ip_address=scan_data.get("ip_address"),
                user_agent=scan_data.get("user_agent"),
                runtime_ms=scan_data.get("runtime_ms")
            )
            
            self.db.add(scan)
            self.db.commit()
            
            # Log sanitized data
            safe_data = self._sanitize_for_logging(scan_data)
            self.logger.info(
                "Scan completed",
                extra={
                    "scan_id": scan.id,
                    "scan_type": scan.scan_type,
                    "model": scan.model_name,
                    "threat_level": scan.threat_level,
                    "data": safe_data
                }
            )
            
        except Exception as e:
            self.logger.error(
                f"Failed to log scan: {str(e)}",
                extra={"scan_data": self._sanitize_for_logging(scan_data)}
            )
            raise
            
    def log_security_event(self, event_type: str, details: Dict) -> None:
        """Log a security-related event"""
        try:
            safe_details = self._sanitize_for_logging(details)
            self.logger.warning(
                f"Security event: {event_type}",
                extra={
                    "event_type": event_type,
                    "timestamp": datetime.utcnow().isoformat(),
                    "details": safe_details
                }
            )
        except Exception as e:
            self.logger.error(f"Failed to log security event: {str(e)}")
            raise
            
    def log_model_drift(self, model_name: str, drift_data: Dict) -> None:
        """Log model drift detection"""
        try:
            self.logger.info(
                "Model drift detected",
                extra={
                    "model": model_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "drift_data": drift_data
                }
            )
        except Exception as e:
            self.logger.error(f"Failed to log model drift: {str(e)}")
            raise
            
    def get_scan_history(self, 
                        model_name: Optional[str] = None,
                        scan_type: Optional[str] = None,
                        min_threat_level: Optional[float] = None,
                        limit: int = 100) -> List[Dict]:
        """Retrieve scan history with filters"""
        try:
            query = self.db.query(Scan)
            
            if model_name:
                query = query.filter(Scan.model_name == model_name)
            if scan_type:
                query = query.filter(Scan.scan_type == scan_type)
            if min_threat_level is not None:
                query = query.filter(Scan.threat_level >= min_threat_level)
                
            scans = query.order_by(Scan.created_at.desc()).limit(limit).all()
            
            return [
                {
                    "id": scan.id,
                    "scan_type": scan.scan_type,
                    "model_name": scan.model_name,
                    "threat_level": scan.threat_level,
                    "created_at": scan.created_at.isoformat(),
                    "findings": scan.findings
                }
                for scan in scans
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve scan history: {str(e)}")
            raise
            
    def get_model_stats(self, model_name: str) -> Dict:
        """Get statistics for a specific model"""
        try:
            scans = self.db.query(Scan).filter(Scan.model_name == model_name).all()
            
            if not scans:
                return {"error": "No scans found for model"}
                
            threat_levels = [s.threat_level for s in scans if s.threat_level is not None]
            
            return {
                "total_scans": len(scans),
                "avg_threat_level": float(np.mean(threat_levels)) if threat_levels else 0,
                "max_threat_level": float(np.max(threat_levels)) if threat_levels else 0,
                "scan_types": list(set(s.scan_type for s in scans)),
                "first_seen": min(s.created_at for s in scans).isoformat(),
                "last_seen": max(s.created_at for s in scans).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get model stats: {str(e)}")
            raise 