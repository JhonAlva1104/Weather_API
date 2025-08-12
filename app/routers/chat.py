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
        
        # Get clothing recommendations
        clothing_recommendation = ClothingService.get_clothing_recommendations(
            weather_data.temperature,
            weather_data.weather_condition
        )
        
        # Create ClothingRecommendation object
        clothing_rec = ClothingRecommendation(
            location=weather_data.location,
            weather=weather_data,
            recommendations=clothing_recommendation,
            general_advice=f"Based on the current weather in {weather_data.location}, here are my recommendations."
        )
        
        # Get Gemini AI response if question is provided
        gemini_response = None
        if request.question:
            gemini_response = await GeminiService.get_gemini_response(
                weather_data, clothing_rec, request.question
            )
        
        return ChatbotResponse(
            message="Weather and clothing recommendations retrieved successfully",
            clothing_recommendation=clothing_rec,
            gemini_response=gemini_response
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/natural", response_model=dict)
async def natural_chat(request: dict):
    """
    Natural conversation endpoint with Gemini AI - no weather restrictions
    """
    try:
        question = request.get("question", "")
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        # Get natural response from Gemini without weather context
        response = await GeminiService.get_natural_response(question)
        
        return {
            "response": response,
            "type": "natural_conversation"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in natural chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )