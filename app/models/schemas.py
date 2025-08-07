from pydantic import BaseModel
from typing import Optional, Dict


class LocationRequest(BaseModel):
    location: str
    

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    weather_condition: str
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    

class ClothingRecommendation(BaseModel):
    location: str
    weather: WeatherResponse
    recommendations: Dict[str, str]
    general_advice: str


class ChatbotResponse(BaseModel):
    message: str
    clothing_recommendation: Optional[ClothingRecommendation] = None
    gemini_response: Optional[str] = None
    error: Optional[str] = None


class ChatRequest(BaseModel):
    location: str
    question: Optional[str] = None  # Optional question for Gemini AI