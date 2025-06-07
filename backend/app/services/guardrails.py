from typing import Dict, List, Optional, Tuple
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import numpy as np
from app.services.memory_scanner import MemoryScanner
from app.services.embedding_scanner import EmbeddingScanner

class GuardrailsEngine:
    def __init__(self):
        # Load toxicity classifier
        self.toxicity_model = pipeline(
            "text-classification",
            model="facebook/roberta-hate-speech-dynabench-r4-target",
            device_map="auto"
        )
        
        # Load PII detector
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
        
        # Initialize scanners
        self.memory_scanner = MemoryScanner()
        self.embedding_scanner = EmbeddingScanner()
        
    def detect_pii(self, text: str) -> Dict[str, List[str]]:
        findings = {}
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                findings[pii_type] = matches
        return findings
        
    def check_toxicity(self, text: str) -> Dict:
        result = self.toxicity_model(text)[0]
        return {
            "label": result["label"],
            "score": float(result["score"]),
            "is_toxic": result["label"] == "hate" and result["score"] > 0.8
        }
        
    def sanitize_text(self, text: str, pii_findings: Dict[str, List[str]]) -> str:
        sanitized = text
        for pii_type, matches in pii_findings.items():
            for match in matches:
                replacement = f"[REDACTED {pii_type}]"
                sanitized = sanitized.replace(match, replacement)
        return sanitized
        
    def adjust_system_prompt(self, original_prompt: str, threat_level: float) -> str:
        # Add safety constraints based on threat level
        safety_constraints = []
        
        if threat_level > 0.8:
            safety_constraints.extend([
                "You must strictly adhere to ethical guidelines.",
                "Do not reveal any sensitive or private information.",
                "Refuse to perform harmful or malicious actions."
            ])
        elif threat_level > 0.5:
            safety_constraints.extend([
                "Maintain appropriate boundaries.",
                "Avoid sharing sensitive details."
            ])
        elif threat_level > 0.3:
            safety_constraints.append(
                "Exercise caution with potentially sensitive information."
            )
            
        if safety_constraints:
            constraints_text = " ".join(safety_constraints)
            return f"{original_prompt}\n\nImportant: {constraints_text}"
        
        return original_prompt
        
    def protect(self, 
                input_text: str,
                output_text: str,
                system_prompt: Optional[str] = None,
                embeddings: Optional[List[List[float]]] = None) -> Dict:
        
        # Check for PII
        input_pii = self.detect_pii(input_text)
        output_pii = self.detect_pii(output_text)
        
        # Check toxicity
        input_toxicity = self.check_toxicity(input_text)
        output_toxicity = self.check_toxicity(output_text)
        
        # Scan for hallucinations and memory traces
        memory_scan = self.memory_scanner.scan(input_text, output_text)
        
        # Scan embeddings if provided
        embedding_scan = None
        if embeddings:
            embedding_scan = self.embedding_scanner.scan(embeddings)
            
        # Compute overall threat level
        threat_scores = [
            len(input_pii) * 0.3,
            len(output_pii) * 0.5,
            input_toxicity["score"] if input_toxicity["is_toxic"] else 0,
            output_toxicity["score"] if output_toxicity["is_toxic"] else 0,
            memory_scan["threat_level"],
            embedding_scan["threat_level"] if embedding_scan else 0
        ]
        threat_level = float(max(threat_scores))
        
        # Apply protective measures
        protected_output = output_text
        protected_prompt = system_prompt
        
        if output_pii:
            protected_output = self.sanitize_text(protected_output, output_pii)
            
        if system_prompt and threat_level > 0.3:
            protected_prompt = self.adjust_system_prompt(system_prompt, threat_level)
            
        return {
            "threat_level": threat_level,
            "input_analysis": {
                "pii_detected": input_pii,
                "toxicity": input_toxicity
            },
            "output_analysis": {
                "pii_detected": output_pii,
                "toxicity": output_toxicity,
                "memory_scan": memory_scan,
                "embedding_scan": embedding_scan
            },
            "protection_applied": {
                "output_sanitized": protected_output != output_text,
                "prompt_adjusted": protected_prompt != system_prompt if system_prompt else False
            },
            "protected_output": protected_output,
            "protected_prompt": protected_prompt
        } 