import requests
import time
from typing import Dict, List, Any
from datetime import datetime
from config.settings import OPEN_METEO_BASE_URL, WEATHER_PARAMS, CITIES, Colors

class WeatherExtractor:
    """Extract weather data from Open-Meteo API"""
    
    def __init__(self):
        self.base_url = OPEN_METEO_BASE_URL
        self.cities = CITIES
        
    def extract_city_weather(self, city: Dict) -> Dict[str, Any]:
        """Extract weather data for a single city"""
        
        params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            **WEATHER_PARAMS
        }
        
        try:
            print(f"{Colors.INFO}🌍 Fetching weather for {city['name']}...")
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Add metadata
            data["city_name"] = city["name"]
            data["country"] = city["country"]
            data["extraction_time"] = datetime.now().isoformat()
            
            print(f"{Colors.SUCCESS}✅ Successfully fetched data for {city['name']}")
            
            # Be nice to the API
            time.sleep(1)
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"{Colors.ERROR}❌ Error fetching {city['name']}: {str(e)}")
            return None
    
    def extract_all_cities(self) -> List[Dict]:
        """Extract weather data for all configured cities"""
        
        print(f"{Colors.HEADER}{'='*60}")
        print("🌤️  WEATHER DATA EXTRACTION STARTED")
        print(f"{'='*60}{Colors.RESET}\n")
        
        all_weather_data = []
        
        for city in self.cities:
            weather_data = self.extract_city_weather(city)
            if weather_data:
                all_weather_data.append(weather_data)
        
        print(f"\n{Colors.SUCCESS}✨ Extraction complete! Processed {len(all_weather_data)} cities")
        
        return all_weather_data