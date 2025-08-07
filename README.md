# Weather-Based Clothing Recommendation Chatbot API with Gemini AI

A FastAPI-based chatbot that provides personalized clothing recommendations based on real-time weather data for any location worldwide, enhanced with Google Gemini AI for conversational responses.

## Overview

This API integrates three external services:
- **OpenCage Geocoding API**: Converts location names to geographic coordinates
- **Dragon Weather API**: Provides current weather conditions based on coordinates
- **Google Gemini AI**: Provides intelligent, conversational responses about weather and clothing

The chatbot analyzes weather data (temperature, conditions, humidity) and generates intelligent clothing recommendations. With Gemini AI integration, it can also answer specific questions about weather and provide personalized advice in a conversational manner.

## Features

- 🌍 **Global Location Support**: Works with any location worldwide
- 🌤️ **Real-time Weather Data**: Gets current weather conditions
- 👕 **Smart Recommendations**: Provides detailed clothing suggestions
- 🤖 **Gemini AI Integration**: Conversational responses and personalized advice
- 💬 **Question Answering**: Ask specific questions about weather and clothing
- 🔧 **Robust Error Handling**: Handles API failures and invalid requests
- 📚 **Interactive Documentation**: Auto-generated API docs with Swagger UI
- 🚀 **Fast Performance**: Built with FastAPI for high performance

## API Architecture

### How It Works

1. **Location Processing**: User provides a location name (e.g., "Bogota, Colombia")
2. **Geocoding**: OpenCage API converts the location to latitude/longitude coordinates
3. **Weather Retrieval**: Dragon Weather API fetches current weather data using coordinates
4. **Analysis**: The system analyzes temperature, weather conditions, and humidity
5. **Recommendations**: Generates personalized clothing suggestions
6. **Response**: Returns structured recommendations with explanations

### Recommendation Logic

The system considers multiple factors:

**Temperature Ranges:**
- **< 10°C**: Heavy winter clothing, multiple layers
- **10-20°C**: Light jackets, long sleeves
- **20-25°C**: Comfortable layers, optional light jacket
- **> 25°C**: Light, breathable clothing

**Weather Conditions:**
- **Rain/Drizzle**: Waterproof gear, umbrellas
- **Snow**: Heavy winter coats, waterproof boots
- **Wind**: Wind-resistant jackets
- **High Humidity**: Breathable, moisture-wicking fabrics

## Installation

1. **Clone or download the project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini API Key (Required for enhanced features):**
   
   **Option A: Environment Variable (Recommended)**
   ```bash
   # Windows
   set GEMINI_API_KEY=your_gemini_api_key_here
   
   # Linux/Mac
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **Option B: Create a .env file**
   ```bash
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   ```
   
   **Get your Gemini API key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy and use it in your environment

4. **Run the application:**
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

**Note**: The API will work without a Gemini API key, but the `/chat-enhanced` endpoint will provide fallback responses instead of AI-generated content.

## API Endpoints

### 1. Root Endpoint
**GET** `/`
- Returns API information and available endpoints

### 2. Chat with Gemini AI
**POST** `/chat`
- Provides clothing recommendations with conversational Gemini AI responses
- Supports optional questions for personalized advice
- Focused exclusively on clothing and fashion-related questions

**Chat Request Body:**
```json
{
  "location": "Bogota, Colombia",
  "question": "What should I wear for a business meeting today?"
}
```

**Note**: The `question` field is optional. The chat endpoint is powered by Google Gemini AI and focuses exclusively on clothing and fashion-related questions. If you ask about topics unrelated to clothing, the assistant will politely redirect you.

**Chat Response (with Gemini AI):**
```json
{
  "message": "Here are my clothing recommendations for Bogotá, RAP (Especial) Central, Colombia! Current temperature is 15°C with clear conditions.",
  "clothing_recommendation": {
    "location": "Bogotá, RAP (Especial) Central, Colombia",
    "weather": {
      "location": "Bogotá, RAP (Especial) Central, Colombia",
      "temperature": 15.0,
      "weather_condition": "Clear",
      "humidity": 65.0,
      "wind_speed": 10.0
    },
    "recommendations": {
      "outerwear": "Light jacket or cardigan",
      "layers": "Long-sleeve shirt or light sweater",
      "bottoms": "Long pants or jeans",
      "footwear": "Closed shoes or sneakers",
      "accessories": "Light scarf (optional)"
    },
    "general_advice": "Mild weather - perfect for layering. You can adjust as needed throughout the day."
  },
  "gemini_response": "Perfect weather for a business meeting in Bogotá! At 15°C with clear skies, you'll want to look professional while staying comfortable. I'd recommend a crisp long-sleeve dress shirt or blouse with a lightweight blazer or cardigan that you can easily remove if it warms up. Dark slacks or a business skirt with closed-toe shoes will complete the look. The clear weather means no need for an umbrella, but you might want to keep that light jacket handy for air-conditioned spaces. You'll look sharp and feel comfortable all day!",
  "error": null
}
```

### 4. Weather Data
**GET** `/weather/{location}`
- Returns raw weather data for a location
- Example: `/weather/London`

## Usage Examples

### Using cURL

```bash
# Get clothing recommendations
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"location": "New York, USA", "question": "What should I wear today?"}'

# Get weather data only
curl "http://localhost:8000/weather/Tokyo"
```

### Using Python requests

```python
import requests

# Get clothing recommendations
response = requests.post(
    "http://localhost:8000/chat",
    json={"location": "Paris, France", "question": "What should I wear today?"}
)
print(response.json())

# Get weather data
weather = requests.get("http://localhost:8000/weather/Sydney")
print(weather.json())
```

### Using JavaScript fetch

```javascript
// Get clothing recommendations
fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({location: 'Berlin, Germany', question: 'What should I wear today?'})
})
.then(response => response.json())
.then(data => console.log(data));
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Location not found
- **408 Request Timeout**: API timeout (10 seconds)
- **503 Service Unavailable**: External API connection issues
- **500 Internal Server Error**: Unexpected server errors

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive documentation where you can test the API directly.

## External APIs Used

### OpenCage Geocoding API
- **Purpose**: Convert location names to coordinates
- **Endpoint**: `https://api.opencagedata.com/geocode/v1/json`
- **Features**: Global coverage, detailed location data
- **Rate Limit**: 2,500 requests/day (free tier)

### Dragon Weather API
- **Purpose**: Retrieve current weather conditions
- **Endpoint**: `https://dragon.best/api/glax_weather.json`
- **Features**: Real-time weather data, multiple units
- **Data**: Temperature, conditions, humidity, wind speed

## Development Approach

### Best Practices Implemented

1. **Modular Design**: Separated concerns with dedicated functions
2. **Type Safety**: Used Pydantic models for request/response validation
3. **Error Handling**: Comprehensive exception handling with meaningful messages
4. **Logging**: Structured logging for debugging and monitoring
5. **Documentation**: Auto-generated API documentation
6. **Timeout Handling**: Prevents hanging requests
7. **Input Validation**: Validates all user inputs
8. **Response Models**: Structured, predictable API responses

### Project Structure

The application follows a modular architecture for better scalability and maintainability:

```
API/
├── app/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Environment variables and API configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models for request/response validation
│   ├── routers/
   │   │   ├── __init__.py
   │   │   ├── chat.py              # Chat endpoint (/chat/) with Gemini AI
   │   │   └── weather.py           # Weather endpoints (/weather/{location})
│   └── services/
│       ├── __init__.py
│       ├── clothing_service.py  # Clothing recommendation business logic
│       ├── gemini_service.py    # Gemini AI integration
│       └── weather_service.py   # Weather and geocoding API integration
├── main.py                      # FastAPI app initialization and routing
├── requirements.txt             # Python dependencies
├── test_api.py                  # API testing script
└── README.md                    # This file
```

### Architecture Benefits

- **Separation of Concerns**: Each module has a specific responsibility
- **Scalability**: Easy to add new features and endpoints
- **Maintainability**: Code is organized and easy to navigate
- **Testability**: Services can be tested independently
- **Reusability**: Services can be reused across different endpoints

## Testing the API

1. **Start the server**: `python main.py`
2. **Test basic functionality**: Visit `http://localhost:8000`
3. **Try the chatbot**: POST to `/chat` with a location
4. **Check documentation**: Visit `http://localhost:8000/docs`
5. **Test error handling**: Try invalid locations or network issues

## Future Enhancements

- Add weather forecasts for multi-day recommendations
- Include user preferences (style, activity type)
- Add clothing images or shopping links
- Implement caching for better performance
- Add user authentication and personalization
- Support for multiple languages
- Integration with clothing retailers

## License

This project is for educational and demonstration purposes.