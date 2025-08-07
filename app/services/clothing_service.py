from typing import Dict, Optional


class ClothingService:
    @staticmethod
    def get_clothing_recommendations(temperature: float, weather_condition: str, humidity: Optional[float] = None) -> Dict[str, str]:
        """
        Generate clothing recommendations based on weather conditions
        """
        recommendations = {}
        
        # Temperature-based recommendations
        if temperature < 10:
            recommendations["outerwear"] = "Heavy winter coat or parka"
            recommendations["layers"] = "Thermal underwear, sweater, and warm shirt"
            recommendations["bottoms"] = "Warm pants or thermal leggings"
            recommendations["footwear"] = "Insulated boots or warm shoes"
            recommendations["accessories"] = "Hat, gloves, and warm scarf"
        elif 10 <= temperature < 20:
            recommendations["outerwear"] = "Light jacket or cardigan"
            recommendations["layers"] = "Long-sleeve shirt or light sweater"
            recommendations["bottoms"] = "Long pants or jeans"
            recommendations["footwear"] = "Closed shoes or sneakers"
            recommendations["accessories"] = "Light scarf (optional)"
        elif 20 <= temperature < 25:
            recommendations["outerwear"] = "Light cardigan or no jacket needed"
            recommendations["layers"] = "T-shirt or light long-sleeve"
            recommendations["bottoms"] = "Comfortable pants or light jeans"
            recommendations["footwear"] = "Sneakers or comfortable shoes"
            recommendations["accessories"] = "Sunglasses (optional)"
        else:  # temperature >= 25
            recommendations["outerwear"] = "No jacket needed"
            recommendations["layers"] = "Light t-shirt or tank top"
            recommendations["bottoms"] = "Shorts or light pants"
            recommendations["footwear"] = "Sandals or breathable shoes"
            recommendations["accessories"] = "Sunglasses and hat for sun protection"
        
        # Weather condition adjustments
        weather_lower = weather_condition.lower()
        if "rain" in weather_lower or "drizzle" in weather_lower:
            recommendations["outerwear"] = "Waterproof jacket or raincoat"
            recommendations["accessories"] = recommendations.get("accessories", "") + ", umbrella"
            recommendations["footwear"] = "Waterproof shoes or boots"
        elif "snow" in weather_lower:
            recommendations["outerwear"] = "Heavy winter coat with hood"
            recommendations["footwear"] = "Waterproof winter boots"
            recommendations["accessories"] = "Warm hat, gloves, and scarf"
        elif "wind" in weather_lower:
            recommendations["outerwear"] = "Wind-resistant jacket"
        
        # Humidity adjustments
        if humidity and humidity > 70:
            recommendations["layers"] = "Breathable, moisture-wicking fabrics"
            if temperature > 20:
                recommendations["layers"] += " (avoid heavy materials)"
        
        return recommendations
    
    @staticmethod
    def get_general_advice(temperature: float, weather_condition: str) -> str:
        """
        Generate general clothing advice based on weather
        """
        if temperature < 10:
            advice = "Very cold weather - dress in layers and cover exposed skin. "
            advice += "Don't forget warm accessories like gloves and a hat."
        elif 10 <= temperature < 20:
            advice = "Mild weather - perfect for layering. "
            advice += "You can adjust as needed throughout the day."
        elif 20 <= temperature < 25:
            advice = "Comfortable temperature - light layers work well. "
            advice += "You might want a light jacket for air-conditioned spaces."
        else:
            advice = "Warm weather - choose breathable fabrics and stay hydrated. "
            advice += "Light colors can help reflect heat."
        
        # Add weather-specific advice
        weather_lower = weather_condition.lower()
        if "rain" in weather_lower:
            advice += " Don't forget waterproof gear and an umbrella!"
        elif "snow" in weather_lower:
            advice += " Bundle up and wear waterproof boots for snowy conditions."
        elif "wind" in weather_lower:
            advice += " Consider wind-resistant outer layers."
        elif "sun" in weather_lower or "clear" in weather_lower:
            if temperature > 20:
                advice += " Great weather - don't forget sun protection!"
        
        return advice