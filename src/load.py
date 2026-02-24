import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
from typing import Dict
from config.settings import Colors, DATABASE_URL

class WeatherLoader:
    """Load transformed weather data into database"""
    
    def __init__(self):
        self.connection_string = DATABASE_URL
        self.engine = create_engine(self.connection_string)
        
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"{Colors.SUCCESS}✅ Database connection successful")
            return True
        except Exception as e:
            print(f"{Colors.ERROR}❌ Database connection failed: {str(e)}")
            return False
    
    def create_tables(self):
        """Create tables if they don't exist"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL,
            timezone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(latitude, longitude)
        );
        
        CREATE TABLE IF NOT EXISTS current_weather (
            weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            temperature REAL,
            feels_like REAL,
            humidity INTEGER,
            pressure INTEGER,
            wind_speed REAL,
            wind_direction INTEGER,
            weather_code INTEGER,
            weather_description TEXT,
            uv_index REAL,
            visibility REAL,
            recorded_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(location_id) REFERENCES locations(location_id)
        );
        
        CREATE TABLE IF NOT EXISTS hourly_forecast (
            forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            forecast_time TIMESTAMP,
            temperature REAL,
            feels_like REAL,
            precipitation_probability INTEGER,
            precipitation REAL,
            weather_code INTEGER,
            wind_speed REAL,
            wind_direction INTEGER,
            humidity INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(location_id) REFERENCES locations(location_id)
        );
        
        CREATE TABLE IF NOT EXISTS daily_forecast (
            forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            forecast_date DATE,
            temperature_max REAL,
            temperature_min REAL,
            sunrise TIME,
            sunset TIME,
            precipitation_sum REAL,
            precipitation_probability_max INTEGER,
            weather_code INTEGER,
            wind_speed_max REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(location_id) REFERENCES locations(location_id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_current_weather_recorded ON current_weather(recorded_at);
        CREATE INDEX IF NOT EXISTS idx_hourly_forecast_time ON hourly_forecast(forecast_time);
        CREATE INDEX IF NOT EXISTS idx_daily_forecast_date ON daily_forecast(forecast_date);
        """
        
        with self.engine.connect() as conn:
            # Split SQL statements and execute each one
            for statement in create_table_sql.split(';'):
                if statement.strip():
                    conn.execute(text(statement))
            conn.commit()
        print(f"{Colors.SUCCESS}✅ Tables created successfully")
    
    def load_locations(self, current_df: pd.DataFrame) -> Dict[str, int]:
        """Load unique locations and return location IDs"""
        
        location_ids = {}
        
        # Get unique locations
        locations = current_df[['city', 'country', 'latitude', 'longitude', 'timezone']].drop_duplicates()
        
        with self.engine.connect() as conn:
            for _, location in locations.iterrows():
                # Check if location exists
                query = text("""
                    SELECT location_id FROM locations 
                    WHERE latitude = :lat AND longitude = :lon
                """)
                
                result = conn.execute(query, {"lat": location['latitude'], "lon": location['longitude']}).fetchone()
                
                if result:
                    location_ids[location['city']] = result[0]
                else:
                    # Insert new location
                    insert_query = text("""
                        INSERT INTO locations (city, country, latitude, longitude, timezone)
                        VALUES (:city, :country, :lat, :lon, :tz)
                        RETURNING location_id
                    """)
                    
                    result = conn.execute(insert_query, {
                        "city": location['city'],
                        "country": location['country'],
                        "lat": location['latitude'],
                        "lon": location['longitude'],
                        "tz": location['timezone']
                    })
                    
                    location_ids[location['city']] = result.fetchone()[0]
            
            # Commit all changes at once
            conn.commit()
        
        print(f"{Colors.SUCCESS}📍 Loaded {len(location_ids)} locations")
        return location_ids
    
    def load_current_weather(self, df: pd.DataFrame, location_ids: Dict[str, int]) -> None:
        """Load current weather data"""
        
        # Add location_id to dataframe
        df['location_id'] = df['city'].map(location_ids)
        
        # Select and rename columns for database
        columns = ['location_id', 'temperature', 'feels_like', 'humidity', 'pressure',
                  'wind_speed', 'wind_direction', 'weather_code', 'weather_description',
                  'uv_index', 'visibility', 'recorded_at']
        
        df_to_load = df[columns].copy()
        
        # Load to database
        df_to_load.to_sql('current_weather', self.engine, if_exists='append', index=False)
        
        print(f"{Colors.SUCCESS}🌡️  Loaded {len(df_to_load)} current weather records")
    
    def load_hourly_forecast(self, df: pd.DataFrame, location_ids: Dict[str, int]) -> None:
        """Load hourly forecast data"""
        
        if df.empty:
            print(f"{Colors.WARNING}⚠️ No hourly forecast data to load")
            return
        
        # Add location_id to dataframe
        df['location_id'] = df['city'].map(location_ids)
        
        # Select and rename columns
        columns = ['location_id', 'forecast_time', 'temperature', 'feels_like',
                  'precipitation_probability', 'precipitation', 'weather_code',
                  'wind_speed', 'wind_direction', 'humidity']
        
        df_to_load = df[columns].copy()
        
        # Load to database
        df_to_load.to_sql('hourly_forecast', self.engine, if_exists='append', index=False)
        
        print(f"{Colors.SUCCESS}⏰ Loaded {len(df_to_load)} hourly forecast records")
    
    def load_daily_forecast(self, df: pd.DataFrame, location_ids: Dict[str, int]) -> None:
        """Load daily forecast data"""
        
        if df.empty:
            print(f"{Colors.WARNING}⚠️ No daily forecast data to load")
            return
        
        # Add location_id to dataframe
        df['location_id'] = df['city'].map(location_ids)
        
        # Select and rename columns
        columns = ['location_id', 'forecast_date', 'temperature_max', 'temperature_min',
                  'sunrise', 'sunset', 'precipitation_sum', 'precipitation_probability_max',
                  'weather_code', 'wind_speed_max']
        
        df_to_load = df[columns].copy()
        
        # Convert time columns to string if needed
        if 'sunrise' in df_to_load.columns:
            df_to_load['sunrise'] = df_to_load['sunrise'].astype(str).str.split('T').str[1]
            df_to_load['sunset'] = df_to_load['sunset'].astype(str).str.split('T').str[1]
        
        # Load to database
        df_to_load.to_sql('daily_forecast', self.engine, if_exists='append', index=False)
        
        print(f"{Colors.SUCCESS}📅 Loaded {len(df_to_load)} daily forecast records")
    
    def load_all(self, current_df: pd.DataFrame, hourly_df: pd.DataFrame, daily_df: pd.DataFrame) -> None:
        """Load all transformed data"""
        
        print(f"\n{Colors.HEADER}{'='*60}")
        print("💾 DATA LOADING STARTED")
        print(f"{'='*60}{Colors.RESET}\n")
        
        # Test connection
        if not self.test_connection():
            return
        
        try:
            # Create tables first
            self.create_tables()
            
            # Load locations
            location_ids = self.load_locations(current_df)
            
            # Load weather data
            self.load_current_weather(current_df, location_ids)
            self.load_hourly_forecast(hourly_df, location_ids)
            self.load_daily_forecast(daily_df, location_ids)
            
            print(f"\n{Colors.SUCCESS}✨ All data loaded successfully!")
            
        except Exception as e:
            print(f"{Colors.ERROR}❌ Error loading data: {str(e)}")
            raise