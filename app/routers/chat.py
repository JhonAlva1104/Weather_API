from fastapi import APIRouter, HTTPException
import logging
from typing import Optional

from app.models.schemas import (
    LocationRequest,
    ChatRequest,
    ChatbotResponse,
    ClothingRecommendation
)
from app.services.weather_service import WeatherService
from app.services.clothing_service import ClothingService
from app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/", response_model=ChatbotResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint with Gemini AI integration for clothing recommendations
    """
    try:
        # Get weather data
        weather_data = await WeatherService.get_weather_for_location(request.location)
        
        # Generate clothing recommendations
        recommendations = ClothingService.get_clothing_recommendations(
            weather_data.temperature,
            weather_data.weather_condition,
            weather_data.humidity
        )
        general_advice = ClothingService.get_general_advice(
            weather_data.temperature,
            weather_data.weather_condition
        )
        
        # Create clothing recommendation object
        clothing_recommendation = ClothingRecommendation(
            location=weather_data.location,
            weather=weather_data,
            recommendations=recommendations,
            general_advice=general_advice
        )
        
        # Get Gemini AI response
        gemini_response = await GeminiService.get_gemini_response(
            weather_data,
            clothing_recommendation,
            request.question
        )
        
        message = f"Here are my clothing recommendations for {weather_data.location}! "
        message += f"Current temperature is {weather_data.temperature}°C with {weather_data.weather_condition.lower()} conditions."
        
        return ChatbotResponse(
            message=message,
            clothing_recommendation=clothing_recommendation,
            gemini_response=gemini_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat_enhanced: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")