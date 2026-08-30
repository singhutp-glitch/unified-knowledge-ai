from fastapi import FastAPI

app = FastAPI(title="Unified Knowledge AI")


@app.get("/")
def root():
    return {
        "message": "Unified Knowledge AI backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }