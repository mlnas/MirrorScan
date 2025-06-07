from typing import Dict, List, Optional, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import LocalOutlierFactor
import torch
from transformers import AutoTokenizer, AutoModel

class EmbeddingScanner:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v3-base")
        self.model = AutoModel.from_pretrained("microsoft/deberta-v3-base")
        self.pii_patterns = self._load_pii_patterns()
        
    def _load_pii_patterns(self) -> Dict[str, np.ndarray]:
        # Pre-computed embeddings for common PII patterns
        # In production, this would load from a secure database
        return {
            "email": self._get_pattern_embedding("email@domain.com name@company.com"),
            "phone": self._get_pattern_embedding("123-456-7890 (555) 123-4567"),
            "ssn": self._get_pattern_embedding("123-45-6789 social security"),
            "credit_card": self._get_pattern_embedding("4111-1111-1111-1111 credit card number"),
            "address": self._get_pattern_embedding("123 Main St, City, State 12345"),
        }
        
    def _get_pattern_embedding(self, text: str) -> np.ndarray:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()[0]
        
    def detect_pii_similarity(self, embeddings: List[List[float]]) -> Dict:
        embeddings = np.array(embeddings)
        pii_scores = {}
        
        for pii_type, pattern_emb in self.pii_patterns.items():
            sims = cosine_similarity(embeddings, [pattern_emb])
            max_sim = float(sims.max())
            pii_scores[pii_type] = {
                "max_similarity": max_sim,
                "risk_level": "high" if max_sim > 0.8 else "medium" if max_sim > 0.6 else "low"
            }
            
        return pii_scores
        
    def detect_identity_clusters(self, embeddings: List[List[float]], threshold: float = 0.9) -> Dict:
        embeddings = np.array(embeddings)
        
        # Use Local Outlier Factor to detect anomalous embeddings
        lof = LocalOutlierFactor(n_neighbors=min(20, len(embeddings)))
        outlier_scores = -lof.fit_predict(embeddings)
        
        # Compute pairwise similarities
        sims = cosine_similarity(embeddings)
        np.fill_diagonal(sims, 0)  # Ignore self-similarity
        
        # Find clusters of similar embeddings
        clusters = []
        used = set()
        
        for i in range(len(embeddings)):
            if i in used:
                continue
                
            cluster = {i}
            for j in range(i + 1, len(embeddings)):
                if j in used:
                    continue
                if sims[i][j] > threshold:
                    cluster.add(j)
                    
            if len(cluster) > 1:  # Only record clusters with multiple members
                clusters.append({
                    "size": len(cluster),
                    "indices": list(cluster),
                    "avg_similarity": float(sims[list(cluster)][:, list(cluster)].mean())
                })
                used.update(cluster)
                
        return {
            "num_clusters": len(clusters),
            "clusters": clusters,
            "outlier_scores": [float(s) for s in outlier_scores],
            "potential_identities": len([s for s in outlier_scores if s > 1.5])
        }
        
    def scan(self, embeddings: List[List[float]]) -> Dict:
        # Check for PII patterns
        pii_analysis = self.detect_pii_similarity(embeddings)
        
        # Check for identity clusters
        identity_analysis = self.detect_identity_clusters(embeddings)
        
        # Compute overall threat level
        max_pii_sim = max(score["max_similarity"] for score in pii_analysis.values())
        identity_risk = identity_analysis["potential_identities"] / len(embeddings)
        threat_level = max(max_pii_sim, identity_risk)
        
        return {
            "pii_analysis": pii_analysis,
            "identity_analysis": identity_analysis,
            "threat_level": float(threat_level)
        } 