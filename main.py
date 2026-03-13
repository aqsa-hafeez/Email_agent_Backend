import sys
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.gmail_routes import router
import uvicorn

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")

app = FastAPI(title="AI Email Agent API")

# Middleware
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Root Route (404 fix karne ke liye)
@app.get("/")
async def root():
    return {
        "message": "AI Email Agent Backend is Live!",
        "status": "Running",
        "docs": "/docs"
    }

# API Routes
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    # Hugging Face PORT environment variable use karta hai
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)