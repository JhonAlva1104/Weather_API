from fastapi import APIRouter, HTTPException
import logging

from app.services.weather_service import WeatherService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)


@router.get("/{location}")
async def get_weather(location: str):
    """
    Get weather data for a specific location (GET request example)
    """
    try:
        # Get coordinates
        lat, lng, formatted_location = await WeatherService.get_coordinates(location)
        
        # Get weather data
        weather_data = await WeatherService.get_weather_data(lat, lng)
        
        return weather_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_weather: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))