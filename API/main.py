from fastapi import FastAPI

app = FastAPI(
    title="Cloud Pipeline API",
    version="1.0.0"
)

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}
