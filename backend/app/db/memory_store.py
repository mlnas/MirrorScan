from typing import Dict, List, Optional
from datetime import datetime
from app.models.scan import ScanStatus, VulnerabilityType

class MemoryStore:
    def __init__(self):
        self.scans: Dict[int, dict] = {}
        self.vulnerabilities: Dict[int, List[dict]] = {}
        self._scan_id_counter = 1
        self._vuln_id_counter = 1

    def create_scan(self, model_name: str, model_type: str, api_endpoint: str) -> dict:
        scan_id = self._scan_id_counter
        self._scan_id_counter += 1
        
        scan = {
            "id": scan_id,
            "model_name": model_name,
            "model_type": model_type,
            "api_endpoint": api_endpoint,
            "status": ScanStatus.PENDING,
            "risk_score": None,
            "scan_results": None,
            "error_message": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        self.scans[scan_id] = scan
        self.vulnerabilities[scan_id] = []
        return scan

    def get_scan(self, scan_id: int) -> Optional[dict]:
        return self.scans.get(scan_id)

    def list_scans(self, skip: int = 0, limit: int = 100) -> List[dict]:
        scans = list(self.scans.values())
        return scans[skip:skip + limit]

    def update_scan(self, scan_id: int, **kwargs) -> Optional[dict]:
        if scan_id not in self.scans:
            return None
            
        scan = self.scans[scan_id]
        for key, value in kwargs.items():
            if hasattr(scan, key):
                scan[key] = value
        scan["updated_at"] = datetime.utcnow()
        return scan

    def delete_scan(self, scan_id: int) -> bool:
        if scan_id not in self.scans:
            return False
            
        del self.scans[scan_id]
        del self.vulnerabilities[scan_id]
        return True

    def add_vulnerability(self, scan_id: int, vulnerability_type: VulnerabilityType,
                         severity: float, description: str, evidence: dict,
                         remediation: str) -> Optional[dict]:
        if scan_id not in self.vulnerabilities:
            return None
            
        vuln_id = self._vuln_id_counter
        self._vuln_id_counter += 1
        
        vulnerability = {
            "id": vuln_id,
            "scan_id": scan_id,
            "vulnerability_type": vulnerability_type,
            "severity": severity,
            "description": description,
            "evidence": evidence,
            "remediation": remediation,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        self.vulnerabilities[scan_id].append(vulnerability)
        return vulnerability

    def get_vulnerabilities(self, scan_id: int) -> List[dict]:
        return self.vulnerabilities.get(scan_id, []) 