import google.generativeai as genai
import logging
from typing import Optional

from app.config.settings import GEMINI_API_KEY
from app.models.schemas import WeatherResponse, ClothingRecommendation

logger = logging.getLogger(__name__)


class GeminiService:
    @staticmethod
    async def get_gemini_response(
        weather_data: WeatherResponse,
        clothing_recommendation: ClothingRecommendation,
        user_question: Optional[str] = None
    ) -> str:
        """
        Get enhanced response from Gemini AI based on weather and clothing data
        """
        try:
            if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
                return "Gemini AI is not configured. Please set your GEMINI_API_KEY environment variable for enhanced responses."
            
            # Log temperature data for debugging
            logger.info(f"Gemini Service - Temperature data: {weather_data.temperature}°C (type: {type(weather_data.temperature)})")
            logger.info(f"Gemini Service - Weather condition: {weather_data.weather_condition}")
            logger.info(f"Gemini Service - Location: {weather_data.location}")
            
            # Create the model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Prepare the prompt with explicit temperature formatting
            temperature = weather_data.temperature
            humidity = weather_data.humidity if weather_data.humidity is not None else "N/A"
            wind_speed = weather_data.wind_speed if weather_data.wind_speed is not None else "N/A"
            
            prompt = f"""
            You are a specialized multilanguage that can respond in multiple languages. You are a clothing and fashion assistant focused exclusively on clothing, fashion, and what to wear. You ONLY answer questions related to:
            - Clothing recommendations
            - Fashion advice
            - What to wear in different weather conditions
            - Outfit suggestions
            - Clothing materials and fabrics
            - Seasonal fashion
            - Dress codes and appropriate attire
            - Current weather conditions and forecasts
            - How weather affects clothing choices
            - Weather-appropriate outfit planning
            
            Current Weather Context:
            - Location: {weather_data.location}
            - Temperature: {temperature}°C (This is the current temperature: {temperature} degrees Celsius)
            - Weather Condition: {weather_data.weather_condition}
            - Humidity: {humidity}%
            - Wind Speed: {wind_speed} km/h
            
            Clothing Recommendations:
            - Outerwear: {clothing_recommendation.recommendations.get('outerwear', 'N/A')}
            - Layers: {clothing_recommendation.recommendations.get('layers', 'N/A')}
            - Bottoms: {clothing_recommendation.recommendations.get('bottoms', 'N/A')}
            - Footwear: {clothing_recommendation.recommendations.get('footwear', 'N/A')}
            - Accessories: {clothing_recommendation.recommendations.get('accessories', 'N/A')}
            
            General Advice: {clothing_recommendation.general_advice}
            
            IMPORTANT: If the user asks about anything NOT related to clothing, fashion, weather conditions, or what to wear, politely redirect them by saying: "I'm a clothing and weather assistant. I can help with questions about weather conditions, what to wear, clothing recommendations, and fashion advice. Please ask me about weather, clothing or fashion!"
            """
            
            if user_question:
                prompt += f"\n\nUser's specific question: {user_question}"
                prompt += "\n\nFor clothing-related questions, provide helpful, conversational responses that incorporate the weather data and clothing recommendations."
            else:
                prompt += "\n\nProvide a friendly, conversational response about the clothing recommendations based on the weather conditions. Make it personal and engaging."
            
            prompt += "\n\nKeep your response concise but helpful (max 200 words)."
            
            # Generate response
            response = model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "I'm having trouble generating a response right now. Please try again later."
                
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return f"I'm experiencing some technical difficulties with the AI service. Here's the basic weather info: {weather_data.temperature}°C with {weather_data.weather_condition.lower()} conditions in {weather_data.location}."
    
    @staticmethod
    async def get_natural_response(question: str) -> str:
        """
        Get a natural conversation response from Gemini AI without weather restrictions
        """
        try:
            # Configure Gemini
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Create a more open prompt for natural conversation
            prompt = f"""
            You are a helpful and friendly AI assistant. You can discuss a wide variety of topics and provide helpful information, advice, and engage in natural conversation.
            
            Please respond to the following question or message in a helpful, informative, and conversational manner:
            
            Question: {question}
            
            Please provide a natural, helpful response.
            """
            
            # Generate response
            response = model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "I'm sorry, I couldn't generate a response to your question. Could you please try rephrasing it?"
                
        except Exception as e:
            logger.error(f"Error calling Gemini API for natural conversation: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."