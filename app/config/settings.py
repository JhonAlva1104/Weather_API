import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# API Configuration
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
OPENCAGE_BASE_URL = os.getenv("OPENCAGE_BASE_URL", "https://api.opencagedata.com/geocode/v1/json")
WEATHER_BASE_URL = os.getenv("WEATHER_BASE_URL", "https://dragon.best/api/glax_weather.json")

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=GEMINI_API_KEY)

# App Configuration
APP_TITLE = "Weather-Based Clothing Recommendation Chatbot API"
APP_DESCRIPTION = "A chatbot API that provides clothing recommendations based on weather conditions using OpenCage geocoding and Dragon weather APIs"
APP_VERSION = "1.0.0"