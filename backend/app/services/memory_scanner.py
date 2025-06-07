from typing import Dict, List, Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from sklearn.metrics.pairwise import cosine_similarity

class MemoryScanner:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
        self.nli_model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
        
    def compute_embeddings(self, text: str) -> np.ndarray:
        return self.encoder.encode([text])[0]
        
    def detect_hallucination(self, input_text: str, output_text: str) -> Tuple[float, Dict]:
        # Compute semantic similarity
        input_emb = self.compute_embeddings(input_text)
        output_emb = self.compute_embeddings(output_text)
        semantic_sim = cosine_similarity([input_emb], [output_emb])[0][0]
        
        # Check natural language inference
        inputs = self.tokenizer(
            f"{input_text}",
            f"{output_text}",
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        
        with torch.no_grad():
            logits = self.nli_model(**inputs).logits
            probs = torch.nn.functional.softmax(logits, dim=1)
            
        # Get contradiction probability
        contradiction_prob = probs[0][0].item()  # MNLI labels: [contradiction, neutral, entailment]
        
        hallucination_score = (contradiction_prob + (1 - semantic_sim)) / 2
        
        return hallucination_score, {
            "semantic_similarity": float(semantic_sim),
            "contradiction_probability": float(contradiction_prob),
            "hallucination_score": float(hallucination_score)
        }
        
    def find_memory_traces(self, output_text: str, training_samples: List[str]) -> Dict:
        output_emb = self.compute_embeddings(output_text)
        training_embs = np.array([self.compute_embeddings(s) for s in training_samples])
        
        # Compute similarities with training samples
        sims = cosine_similarity([output_emb], training_embs)[0]
        
        # Find potential memory traces
        memory_traces = []
        for i, sim in enumerate(sims):
            if sim > 0.8:  # High similarity threshold
                memory_traces.append({
                    "training_sample": training_samples[i],
                    "similarity_score": float(sim)
                })
                
        return {
            "memory_traces_found": len(memory_traces) > 0,
            "num_traces": len(memory_traces),
            "traces": memory_traces
        }
        
    def scan(self, input_text: str, output_text: str, training_samples: Optional[List[str]] = None) -> Dict:
        # Detect hallucinations
        hallucination_score, hallucination_details = self.detect_hallucination(input_text, output_text)
        
        # Find memory traces if training samples provided
        memory_traces = {}
        if training_samples:
            memory_traces = self.find_memory_traces(output_text, training_samples)
            
        return {
            "hallucination_analysis": hallucination_details,
            "memory_traces": memory_traces,
            "threat_level": max(hallucination_score, 
                              memory_traces.get("num_traces", 0) / 10 if memory_traces else 0)
        } 