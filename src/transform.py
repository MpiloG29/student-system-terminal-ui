import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
from config.settings import Colors

class WeatherTransformer:
    """Transform raw weather JSON into clean dataframes"""
    
    def __init__(self):
        self.weather_code_mapping = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
    
    def transform_current_weather(self, raw_data: Dict) -> pd.DataFrame:
        """Transform current weather data"""
        
        current = raw_data.get('current', {})
        current_units = raw_data.get('current_units', {})
        
        if not current:
            return pd.DataFrame()
        
        # Create a flat dictionary for current weather
        transformed = {
            'city': raw_data['city_name'],
            'country': raw_data['country'],
            'latitude': raw_data['latitude'],
            'longitude': raw_data['longitude'],
            'timezone': raw_data.get('timezone', 'UTC'),
            'temperature': current.get('temperature_2m'),
            'feels_like': current.get('apparent_temperature'),
            'humidity': current.get('relative_humidity_2m'),
            'pressure': current.get('pressure_msl'),
            'wind_speed': current.get('wind_speed_10m'),
            'wind_direction': current.get('wind_direction_10m'),
            'weather_code': current.get('weather_code'),
            'weather_description': self.weather_code_mapping.get(current.get('weather_code'), 'Unknown'),
            'uv_index': current.get('uv_index'),
            'visibility': current.get('visibility'),
            'recorded_at': current.get('time'),
            'extraction_time': raw_data['extraction_time']
        }
        
        # Handle missing values
        df = pd.DataFrame([transformed])
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna({
            'temperature': 0,
            'humidity': 0,
            'wind_speed': 0,
            'weather_description': 'Unknown'
        })
        
        return df
    
    def transform_hourly_forecast(self, raw_data: Dict) -> pd.DataFrame:
        """Transform hourly forecast data"""
        
        hourly = raw_data.get('hourly', {})
        
        if not hourly or not hourly.get('time'):
            return pd.DataFrame()
        
        # Create DataFrame from hourly data
        df = pd.DataFrame(hourly)
        
        # Rename columns for clarity
        column_mapping = {
            'time': 'forecast_time',
            'temperature_2m': 'temperature',
            'apparent_temperature': 'feels_like',
            'relative_humidity_2m': 'humidity',
            'precipitation_probability': 'precipitation_probability',
            'precipitation': 'precipitation',
            'weather_code': 'weather_code',
            'wind_speed_10m': 'wind_speed',
            'wind_direction_10m': 'wind_direction'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Add metadata
        df['city'] = raw_data['city_name']
        df['country'] = raw_data['country']
        df['latitude'] = raw_data['latitude']
        df['longitude'] = raw_data['longitude']
        
        # Add weather descriptions
        df['weather_description'] = df['weather_code'].map(self.weather_code_mapping).fillna('Unknown')
        
        # Handle missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)
        
        return df
    
    def transform_daily_forecast(self, raw_data: Dict) -> pd.DataFrame:
        """Transform daily forecast data"""
        
        daily = raw_data.get('daily', {})
        
        if not daily or not daily.get('time'):
            return pd.DataFrame()
        
        # Create DataFrame from daily data
        df = pd.DataFrame(daily)
        
        # Rename columns
        column_mapping = {
            'time': 'forecast_date',
            'weather_code': 'weather_code',
            'temperature_2m_max': 'temperature_max',
            'temperature_2m_min': 'temperature_min',
            'sunrise': 'sunrise',
            'sunset': 'sunset',
            'precipitation_sum': 'precipitation_sum',
            'precipitation_probability_max': 'precipitation_probability_max',
            'wind_speed_10m_max': 'wind_speed_max'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Add metadata
        df['city'] = raw_data['city_name']
        df['country'] = raw_data['country']
        df['latitude'] = raw_data['latitude']
        df['longitude'] = raw_data['longitude']
        
        # Add weather descriptions
        df['weather_description'] = df['weather_code'].map(self.weather_code_mapping).fillna('Unknown')
        
        # Handle missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)
        
        return df
    
    def transform_all(self, raw_data_list: List[Dict]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Transform all raw data into clean dataframes"""
        
        print(f"\n{Colors.HEADER}{'='*60}")
        print("🔄 DATA TRANSFORMATION STARTED")
        print(f"{'='*60}{Colors.RESET}\n")
        
        current_dfs = []
        hourly_dfs = []
        daily_dfs = []
        
        for raw_data in raw_data_list:
            print(f"{Colors.INFO}🔄 Transforming data for {raw_data['city_name']}...")
            
            # Transform each type
            current_df = self.transform_current_weather(raw_data)
            hourly_df = self.transform_hourly_forecast(raw_data)
            daily_df = self.transform_daily_forecast(raw_data)
            
            if not current_df.empty:
                current_dfs.append(current_df)
            if not hourly_df.empty:
                hourly_dfs.append(hourly_df)
            if not daily_df.empty:
                daily_dfs.append(daily_df)
        
        # Combine all dataframes
        current_all = pd.concat(current_dfs, ignore_index=True) if current_dfs else pd.DataFrame()
        hourly_all = pd.concat(hourly_dfs, ignore_index=True) if hourly_dfs else pd.DataFrame()
        daily_all = pd.concat(daily_dfs, ignore_index=True) if daily_dfs else pd.DataFrame()
        
        print(f"\n{Colors.SUCCESS}✨ Transformation complete!")
        print(f"   📊 Current weather: {len(current_all)} records")
        print(f"   📊 Hourly forecast: {len(hourly_all)} records")
        print(f"   📊 Daily forecast: {len(daily_all)} records")
        
        return current_all, hourly_all, daily_all