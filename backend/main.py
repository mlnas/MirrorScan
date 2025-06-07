from fastapi import FastAPI

app = FastAPI(
    title="MirrorScan",
    description="AI Model Security Scanner",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "MirrorScan API is running"} 