from fastapi import FastAPI

app = FastAPI(
    title="AccessFlow API",
    description="API for automating employee onboarding and offboarding.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AccessFlow!"}