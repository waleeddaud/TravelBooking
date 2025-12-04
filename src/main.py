"""
Travel Booking API - Main Application

FastAPI application for flight and hotel booking with JWT authentication.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.routes import auth, search, bookings, users


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Travel Booking API with authentication, search, and booking management",
    version="1.0.0",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(search.router)
app.include_router(bookings.router)
app.include_router(users.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API health check.
    
    Returns:
        Welcome message and API information
    """
    return {
        "message": "Welcome to Travel Booking API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "status": "running"
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        API health status
    """
    return {
        "status": "healthy",
        "api": settings.APP_NAME
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
