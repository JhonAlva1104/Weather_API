import requests
import logging
from typing import Tuple, Optional, Dict, Any
from fastapi import HTTPException

from app.config.settings import OPENCAGE_API_KEY, OPENCAGE_BASE_URL, WEATHER_BASE_URL
from app.models.schemas import WeatherResponse

logger = logging.getLogger(__name__)


class WeatherService:
    @staticmethod
    async def get_coordinates(location: str) -> Tuple[float, float, str]:
        """
        Get coordinates from location using OpenCage API
        Returns: (latitude, longitude, formatted_location)
        """
        logger.info(f"Getting coordinates for location: {location}")
        
        geocode_params = {
            "q": location,
            "key": OPENCAGE_API_KEY,
            "limit": 1
        }
        
        try:
            geocode_response = requests.get(OPENCAGE_BASE_URL, params=geocode_params, timeout=10)
            
            if geocode_response.status_code != 200:
                raise HTTPException(
                    status_code=geocode_response.status_code,
                    detail=f"Geocoding API error: {geocode_response.text}"
                )
            
            geocode_data = geocode_response.json()
            
            if not geocode_data.get("results"):
                raise HTTPException(
                    status_code=404,
                    detail=f"Location '{location}' not found"
                )
            
            # Extract coordinates
            location_data = geocode_data["results"][0]
            lat = location_data["geometry"]["lat"]
            lng = location_data["geometry"]["lng"]
            formatted_location = location_data["formatted"]
            
            logger.info(f"Found coordinates: lat={lat}, lng={lng} for {formatted_location}")
            return lat, lng, formatted_location
            
        except requests.exceptions.Timeout:
            raise HTTPException(status_code=408, detail="Geocoding request timeout - please try again")
        except requests.exceptions.ConnectionError:
            raise HTTPException(status_code=503, detail="Unable to connect to geocoding API")
    
    @staticmethod
    async def get_weather_data(lat: float, lng: float) -> Dict[str, Any]:
        """
        Get weather data using Dragon Weather API
        """
        weather_params = {
            "lat": lat,
            "lon": lng,
            "units": "metric"
        }
        
        try:
            weather_response = requests.get(WEATHER_BASE_URL, params=weather_params, timeout=10)
            
            if weather_response.status_code != 200:
                raise HTTPException(
                    status_code=weather_response.status_code,
                    detail=f"Weather API error: {weather_response.text}"
                )
            
            return weather_response.json()
            
        except requests.exceptions.Timeout:
            raise HTTPException(status_code=408, detail="Weather request timeout - please try again")
        except requests.exceptions.ConnectionError:
            raise HTTPException(status_code=503, detail="Unable to connect to weather API")
    
    @staticmethod
    async def get_weather_for_location(location: str) -> WeatherResponse:
        """
        Get complete weather information for a location
        """
        # Get coordinates
        lat, lng, formatted_location = await WeatherService.get_coordinates(location)
        
        # Get weather data
        weather_data = await WeatherService.get_weather_data(lat, lng)
        
        # Extract weather information - Dragon Weather API returns data directly in root
        if "temperature" not in weather_data:
            raise HTTPException(
                status_code=500,
                detail="Temperature data not available from weather API"
            )
        temperature = weather_data["temperature"]
        weather_condition = weather_data.get("weather", "Clear")
        humidity = weather_data.get("humidity")
        wind_speed = weather_data.get("wind_speed")
        
        # Log extracted weather data for debugging
        logger.info(f"Weather Service - Extracted temperature: {temperature}°C (type: {type(temperature)})")
        logger.info(f"Weather Service - Weather condition: {weather_condition}")
        logger.info(f"Weather Service - Humidity: {humidity}%")
        logger.info(f"Weather Service - Wind speed: {wind_speed} km/h")
        
        return WeatherResponse(
            location=formatted_location,
            temperature=temperature,
            weather_condition=weather_condition,
            humidity=humidity,
            wind_speed=wind_speed
        )