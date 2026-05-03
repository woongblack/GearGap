from fastapi import FastAPI

app = FastAPI(title="GearGap API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the GearGap API"}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
