from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime, timezone
import os
from .config import settings
from .utils import get_cat_fact, get_current_timestamp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Dynamic Profile API",
        "version": settings.VERSION,
        "docs": "/docs",
        "profile_endpoint": "/me"
    }

@app.get("/me")
async def get_profile():
    """Dynamic profile endpoint with cat fact and proper status"""
    try:
        user_email = settings.USER_EMAIL
        user_name = settings.USER_NAME
        user_stack = settings.USER_STACK

        
        # Get cat fact with status information
        cat_fact, fact_status, error_detail = await get_cat_fact()
        
        # Determine overall status
        if fact_status == "success":
            status = "success"
            http_status = 200
        else:
            status = "partial_success"
            http_status = 200  # Or use 207 for multi-status if you prefer
        
        response_data = {
            "status": status,
            "user": {
                "email": user_email,
                "name": user_name,
                "stack": user_stack
            },
            "timestamp": get_current_timestamp(),
            "fact": cat_fact,
        }
        
        # Add error detail if available (optional)
        if error_detail and status != "success":
            response_data["error_detail"] = error_detail
        
        return JSONResponse(content=response_data, status_code=http_status)
        
    except Exception as e:
        logger.error(f"Error in /me endpoint: {e}")
        return JSONResponse(
            content={
                "status": "error",
                "message": "Internal server error",
                "timestamp": get_current_timestamp(),
                "error_detail": str(e)
            },
            status_code=500
        )        
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": get_current_timestamp(),
        "service": settings.PROJECT_NAME
    }

# Custom exception handler
@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "timestamp": get_current_timestamp()
        }
    )