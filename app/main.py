from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router  # Import the router

app = FastAPI(
    title="Intelligent Document Processing API",
    description="Ezitech Case Study AI-004: Automated Document Verification Engine",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the endpoints router with a versioned prefix
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Intelligent Document Processing Engine API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}