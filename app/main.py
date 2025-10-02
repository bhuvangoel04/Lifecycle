# app/main.py

from fastapi import FastAPI
from .auth import auth_router  # Import the auth router

app = FastAPI(
    title="AccessFlow API",
    description="API for automating employee onboarding and offboarding.",
    version="0.1.0"
)

# Include the authentication routes in our main application
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AccessFlow! Navigate to /auth/login to connect your Google account."}