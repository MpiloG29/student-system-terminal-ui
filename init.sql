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