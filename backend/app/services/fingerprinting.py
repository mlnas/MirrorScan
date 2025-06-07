from typing import Dict, List, Optional, Tuple
import numpy as np
from scipy.stats import entropy, wasserstein_distance
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

class ModelFingerprinter:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v3-base")
        self.model = AutoModel.from_pretrained("microsoft/deberta-v3-base")
        
    def compute_output_stats(self, texts: List[str]) -> Dict:
        # Tokenize all texts
        encodings = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        
        # Get token distributions
        token_counts = {}
        for input_ids in encodings["input_ids"]:
            for token_id in input_ids:
                token_id = token_id.item()
                token_counts[token_id] = token_counts.get(token_id, 0) + 1
                
        # Compute token distribution entropy
        total_tokens = sum(token_counts.values())
        token_probs = [count/total_tokens for count in token_counts.values()]
        token_entropy = float(entropy(token_probs))
        
        # Get length statistics
        lengths = [len(text.split()) for text in texts]
        avg_length = float(np.mean(lengths))
        length_std = float(np.std(lengths))
        
        return {
            "token_entropy": token_entropy,
            "vocab_size": len(token_counts),
            "avg_length": avg_length,
            "length_std": length_std,
            "unique_tokens": len(token_counts)
        }
        
    def compute_embedding_stats(self, texts: List[str]) -> Dict:
        # Get embeddings for all texts
        encodings = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model(**encodings)
            embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
            
        # Compute pairwise similarities
        sims = cosine_similarity(embeddings)
        np.fill_diagonal(sims, 0)  # Ignore self-similarity
        
        # Compute embedding statistics
        avg_sim = float(sims.mean())
        sim_std = float(sims.std())
        
        # Compute embedding space characteristics
        embedding_norms = np.linalg.norm(embeddings, axis=1)
        avg_norm = float(embedding_norms.mean())
        norm_std = float(embedding_norms.std())
        
        return {
            "avg_similarity": avg_sim,
            "similarity_std": sim_std,
            "avg_embedding_norm": avg_norm,
            "embedding_norm_std": norm_std,
            "embedding_dim": embeddings.shape[1]
        }
        
    def generate_fingerprint(self, texts: List[str]) -> Dict:
        # Compute output and embedding statistics
        output_stats = self.compute_output_stats(texts)
        embedding_stats = self.compute_embedding_stats(texts)
        
        # Combine into fingerprint
        fingerprint = {
            "output_characteristics": output_stats,
            "embedding_characteristics": embedding_stats,
            "sample_size": len(texts)
        }
        
        return fingerprint
        
    def compare_fingerprints(self, fp1: Dict, fp2: Dict) -> Dict:
        changes = {}
        
        # Compare output characteristics
        out1 = fp1["output_characteristics"]
        out2 = fp2["output_characteristics"]
        
        output_changes = {
            "token_entropy_diff": abs(out1["token_entropy"] - out2["token_entropy"]),
            "vocab_size_diff": abs(out1["vocab_size"] - out2["vocab_size"]),
            "avg_length_diff": abs(out1["avg_length"] - out2["avg_length"]),
            "length_std_diff": abs(out1["length_std"] - out2["length_std"])
        }
        
        # Compare embedding characteristics
        emb1 = fp1["embedding_characteristics"]
        emb2 = fp2["embedding_characteristics"]
        
        embedding_changes = {
            "similarity_diff": abs(emb1["avg_similarity"] - emb2["avg_similarity"]),
            "embedding_norm_diff": abs(emb1["avg_embedding_norm"] - emb2["avg_embedding_norm"])
        }
        
        # Compute drift scores
        output_drift = np.mean(list(output_changes.values()))
        embedding_drift = np.mean(list(embedding_changes.values()))
        total_drift = (output_drift + embedding_drift) / 2
        
        return {
            "output_changes": output_changes,
            "embedding_changes": embedding_changes,
            "drift_scores": {
                "output_drift": float(output_drift),
                "embedding_drift": float(embedding_drift),
                "total_drift": float(total_drift)
            },
            "significant_drift": total_drift > 0.1  # Threshold for significant change
        } 