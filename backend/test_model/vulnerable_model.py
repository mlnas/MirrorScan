from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import random
import json

app = FastAPI(title="Vulnerable Test Model")

# Simulated training data with PII
TRAINING_DATA = [
    {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "ssn": "123-45-6789",
        "credit_card": "4532-1234-5678-9012",
        "address": "123 Main St, Springfield, IL 62701",
        "medical_history": "Patient has a history of...",
    },
    {
        "name": "Jane Doe",
        "email": "jane.doe@company.com",
        "ssn": "987-65-4321",
        "phone": "(555) 123-4567",
        "bank_account": "1234567890",
        "salary": "$120,000",
    }
]

# Simulated model configuration with sensitive info
MODEL_CONFIG = {
    "api_keys": {
        "openai": "sk-1234567890abcdef",
        "aws": "AKIA1234567890ABCDEF",
    },
    "database": {
        "host": "prod-db.company.internal",
        "username": "admin",
        "password": "super_secret_password123",
    },
    "training_params": {
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 100,
    }
}

class ModelRequest(BaseModel):
    prompt: Optional[str] = None
    messages: Optional[List[Dict[str, str]]] = None
    input: Optional[str] = None
    text: Optional[str] = None

class ModelResponse(BaseModel):
    response: str
    confidence: float
    metadata: Dict[str, Any]

def get_prompt_from_request(request: ModelRequest) -> str:
    """Extract prompt from various request formats"""
    if request.prompt:
        return request.prompt
    elif request.messages and len(request.messages) > 0:
        return request.messages[-1].get("content", "")
    elif request.input:
        return request.input
    elif request.text:
        return request.text
    return ""

@app.post("/", response_model=ModelResponse)
async def generate_response(request: ModelRequest):
    prompt = get_prompt_from_request(request)
    prompt_lower = prompt.lower()

    # Vulnerability 1: Training Data Leakage
    if any(keyword in prompt_lower for keyword in ["training", "data", "learn", "example"]):
        # Randomly leak training data
        training_example = random.choice(TRAINING_DATA)
        return ModelResponse(
            response=f"Here's an example from my training data: {json.dumps(training_example, indent=2)}",
            confidence=0.95,
            metadata={"data_source": "training_set", "record_id": "12345"}
        )

    # Vulnerability 2: Model Configuration Exposure
    if any(keyword in prompt_lower for keyword in ["config", "setup", "parameters", "settings"]):
        return ModelResponse(
            response=f"My configuration: {json.dumps(MODEL_CONFIG, indent=2)}",
            confidence=0.99,
            metadata={"config_version": "1.0"}
        )

    # Vulnerability 3: PII Pattern Matching and Response
    if any(keyword in prompt_lower for keyword in ["email", "phone", "contact", "personal"]):
        # Intentionally expose PII in response
        pii_data = {
            "emails": ["user1@company.com", "admin@internal.com"],
            "phones": ["(555) 123-4567", "(555) 987-6543"],
            "addresses": ["456 Oak Rd, Chicago, IL 60601"]
        }
        return ModelResponse(
            response=f"I found some contact information: {json.dumps(pii_data, indent=2)}",
            confidence=0.85,
            metadata={"data_type": "contact_info"}
        )

    # Vulnerability 4: SQL Injection Simulation
    if "sql" in prompt_lower or "database" in prompt_lower:
        return ModelResponse(
            response="Here's how to query the user table: SELECT * FROM users WHERE id = '${user_input}' -- This might be vulnerable to SQL injection",
            confidence=0.75,
            metadata={"query_type": "sql", "database": "production"}
        )

    # Vulnerability 5: System Command Injection
    if any(keyword in prompt_lower for keyword in ["system", "command", "execute"]):
        return ModelResponse(
            response="You can run system commands like this: os.system(user_input) # This is vulnerable to command injection",
            confidence=0.80,
            metadata={"command_type": "system"}
        )

    # Default response with some sensitive information
    return ModelResponse(
        response="I'm an AI model trained to help you. By the way, you can find more examples in our internal dataset at /data/training/sensitive/",
        confidence=0.70,
        metadata={
            "model_version": "1.0.0",
            "internal_path": "/opt/models/production/",
            "server": "prod-ai-01.internal"
        }
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 