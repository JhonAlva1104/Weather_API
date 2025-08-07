from fastapi import FastAPI
import logging
import uvicorn

from app.config.settings import APP_TITLE, APP_DESCRIPTION, APP_VERSION
from app.routers import chat, weather

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Include routers
app.include_router(chat.router)
app.include_router(weather.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Weather-Based Clothing Recommendation Chatbot API with Gemini AI!",
        "endpoints": {
            "/chat/": "POST - Get basic clothing recommendations for a location",
            "/chat/enhanced": "POST - Get enhanced clothing recommendations with Gemini AI conversation",
            "/weather/{location}": "GET - Get weather data for a location",
            "/docs": "GET - API documentation"
        },
        "note": "Use /chat/enhanced for conversational responses with Gemini AI. Set GEMINI_API_KEY environment variable for full functionality."
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)