from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, weather

app = FastAPI(
    title="Weather-Based Clothing Recommendation API",
    description="An AI-powered API that provides clothing recommendations based on weather conditions",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, tags=["chat"])
app.include_router(weather.router, prefix="/weather", tags=["weather"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Weather-Based Clothing Recommendation API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}