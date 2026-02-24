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