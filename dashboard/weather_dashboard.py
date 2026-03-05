import os
import sys
import tempfile
import webbrowser
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import Colors, DATABASE_URL


class WeatherDashboard:
    """Create interactive dashboard from weather data."""

    def __init__(self):
        """Initialize database connection with fallback."""
        self.engine = None
        self.db_type = 'unknown'
        
        try:
            self.engine = create_engine(DATABASE_URL)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.db_type = 'postgresql' if 'postgresql' in DATABASE_URL else 'sqlite'
            print(f"{Colors.SUCCESS}✅ Connected to {self.db_type} database")
        except Exception as e:
            print(f"{Colors.WARNING}⚠️ Could not connect to primary database: {e}")
            # Try SQLite as fallback
            try:
                sqlite_path = os.path.abspath('weather_data.db')
                sqlite_url = f"sqlite:///{sqlite_path}"
                self.engine = create_engine(sqlite_url)
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                self.db_type = 'sqlite'
                print(f"{Colors.SUCCESS}✅ Connected to SQLite fallback database")
            except Exception as e2:
                print(f"{Colors.ERROR}❌ Could not connect to any database: {e2}")
                self.engine = None

    def _execute_query(self, query, params=None, fallback_query=None, fallback_params=None):
        """Execute query with fallback support."""
        if self.engine is None:
            raise ConnectionError("No database connection available")
        
        try:
            if params:
                return pd.read_sql(query, self.engine, params=params)
            return pd.read_sql(query, self.engine)
        except Exception as e:
            print(f"{Colors.WARNING}⚠️ Query failed: {e}")
            if fallback_query:
                try:
                    print(f"{Colors.INFO}↪️ Trying fallback query...")
                    if fallback_params:
                        return pd.read_sql(fallback_query, self.engine, params=fallback_params)
                    return pd.read_sql(fallback_query, self.engine)
                except Exception as e2:
                    print(f"{Colors.ERROR}❌ Fallback also failed: {e2}")
                    return pd.DataFrame()
            return pd.DataFrame()

    def get_current_weather(self):
        """Get latest current weather for all locations."""
        primary_query = text("""
            WITH ranked_current AS (
                SELECT
                    cw.weather_id,
                    cw.location_id,
                    cw.temperature,
                    cw.feels_like,
                    cw.humidity,
                    cw.pressure,
                    cw.wind_speed,
                    cw.weather_description,
                    cw.uv_index,
                    cw.recorded_at,
                    ROW_NUMBER() OVER (
                        PARTITION BY cw.location_id
                        ORDER BY cw.recorded_at DESC, cw.weather_id DESC
                    ) AS rn
                FROM current_weather cw
            )
            SELECT
                l.city,
                l.country,
                l.latitude,
                l.longitude,
                rc.temperature,
                rc.feels_like,
                rc.humidity,
                rc.pressure,
                rc.wind_speed,
                rc.weather_description,
                rc.uv_index,
                rc.recorded_at
            FROM ranked_current rc
            JOIN locations l ON rc.location_id = l.location_id
            WHERE rc.rn = 1
            ORDER BY rc.temperature DESC
        """)

        fallback_query = text("""
            SELECT
                l.city,
                l.country,
                l.latitude,
                l.longitude,
                cw.temperature,
                cw.feels_like,
                cw.humidity,
                cw.pressure,
                cw.wind_speed,
                cw.weather_description,
                cw.uv_index,
                cw.recorded_at
            FROM current_weather cw
            JOIN locations l ON cw.location_id = l.location_id
            WHERE cw.recorded_at = (
                SELECT MAX(cw2.recorded_at)
                FROM current_weather cw2
                WHERE cw2.location_id = cw.location_id
            )
            ORDER BY cw.temperature DESC
        """)

        df = self._execute_query(primary_query, fallback_query=fallback_query)
        
        if df.empty:
            return df
        
        # For SQLite, ensure we have unique cities
        if self.db_type == 'sqlite':
            df = df.sort_values('recorded_at', ascending=False).drop_duplicates(subset=['city'], keep='first')
        
        return df

    def get_weekly_forecast(self, city):
        """Get weekly forecast for a specific city."""
        primary_query = text("""
            WITH ranked_forecast AS (
                SELECT
                    df.location_id,
                    df.forecast_date,
                    df.temperature_max,
                    df.temperature_min,
                    df.precipitation_probability_max AS precipitation_prob,
                    df.wind_speed_max AS wind_speed,
                    ROW_NUMBER() OVER (
                        PARTITION BY df.location_id, df.forecast_date
                        ORDER BY df.created_at DESC, df.forecast_id DESC
                    ) AS rn
                FROM daily_forecast df
            )
            SELECT
                rf.forecast_date,
                rf.temperature_max,
                rf.temperature_min,
                rf.precipitation_prob,
                rf.wind_speed
            FROM ranked_forecast rf
            JOIN locations l ON rf.location_id = l.location_id
            WHERE l.city = :city AND rf.rn = 1
            ORDER BY rf.forecast_date
            LIMIT 7
        """)

        fallback_query = text("""
            SELECT
                df.forecast_date,
                df.temperature_max,
                df.temperature_min,
                df.precipitation_probability_max AS precipitation_prob,
                df.wind_speed_max AS wind_speed
            FROM daily_forecast df
            JOIN locations l ON df.location_id = l.location_id
            WHERE l.city = :city
            ORDER BY df.forecast_date DESC, df.forecast_id DESC
            LIMIT 30
        """)

        df = self._execute_query(primary_query, params={"city": city}, 
                                fallback_query=fallback_query, fallback_params={"city": city})
        
        if df.empty:
            return df
        
        # For SQLite, deduplicate
        if self.db_type == 'sqlite' and len(df) > 7:
            df = df.drop_duplicates(subset=['forecast_date'], keep='first').sort_values('forecast_date').head(7)
        
        return df

    def get_hourly_temperature_trends(self):
        """Get hourly temperature trends for the last 24 hours."""
        # SQLite and PostgreSQL have different datetime functions
        if self.db_type == 'sqlite':
            query = text("""
                SELECT
                    l.city,
                    hf.forecast_time,
                    hf.temperature
                FROM hourly_forecast hf
                JOIN locations l ON hf.location_id = l.location_id
                WHERE datetime(hf.forecast_time) >= datetime('now', '-24 hours')
                ORDER BY hf.forecast_time
            """)
        else:
            query = text("""
                SELECT
                    l.city,
                    hf.forecast_time,
                    hf.temperature
                FROM hourly_forecast hf
                JOIN locations l ON hf.location_id = l.location_id
                WHERE hf.forecast_time >= NOW() - INTERVAL '24 hours'
                ORDER BY hf.forecast_time
            """)
        
        return self._execute_query(query)

    @staticmethod
    def _build_alerts(current_df):
        """Build weather alerts based on current conditions."""
        alerts = []
        for _, row in current_df.iterrows():
            if row['temperature'] >= 35:
                alerts.append(f"🔥 Heat alert in {row['city']} ({row['temperature']:.1f}°C)")
            if row['wind_speed'] >= 35:
                alerts.append(f"💨 High wind in {row['city']} ({row['wind_speed']:.1f} km/h)")
            if row['humidity'] >= 90:
                alerts.append(f"🌧️ Very high humidity in {row['city']} ({row['humidity']:.0f}%)")
        return alerts

    def create_dashboard(self):
        """Create interactive HTML dashboard."""
        print(f"{Colors.INFO}📊 Creating weather dashboard...")
        
        if self.engine is None:
            print(f"{Colors.ERROR}❌ No database connection available. Please run the pipeline first.")
            return None
        
        current_df = self.get_current_weather()
        hourly_trends_df = self.get_hourly_temperature_trends()

        if current_df.empty:
            print(f"{Colors.ERROR}❌ No data available. Please run the pipeline first.")
            return None

        current_df['lat'] = current_df['latitude']
        current_df['lon'] = current_df['longitude']
        current_df['temperature_f'] = (current_df['temperature'] * 9 / 5) + 32

        fig = make_subplots(
            rows=3,
            cols=3,
            subplot_titles=(
                '🌡️ Temperature', '💧 Humidity', '🌪️ Wind Speed',
                '🌍 Global Temperature Map', '🎨 Weather Mix', '📈 Pressure',
                '🔥 Feels Like vs Actual', '☀️ UV Index', '🔗 Temp/Humidity Heatmap'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
                [{'type': 'scattergeo'}, {'type': 'pie'}, {'type': 'bar'}],
                [{'type': 'scatter'}, {'type': 'bar'}, {'type': 'heatmap'}],
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1,
        )

        # Temperature bar chart
        fig.add_trace(
            go.Bar(
                x=current_df['city'], y=current_df['temperature'],
                marker_color=px.colors.qualitative.Bold,
                text=current_df['temperature'].round(1),
                textposition='outside',
                name='Temperature °C',
            ),
            row=1, col=1,
        )

        # Humidity bar chart
        fig.add_trace(
            go.Bar(
                x=current_df['city'], y=current_df['humidity'],
                marker_color='#00E5FF', text=current_df['humidity'].round(0), textposition='outside',
                name='Humidity %',
            ),
            row=1, col=2,
        )

        # Wind speed bar chart
        fig.add_trace(
            go.Bar(
                x=current_df['city'], y=current_df['wind_speed'],
                marker_color='#76FF03', text=current_df['wind_speed'].round(1), textposition='outside',
                name='Wind km/h',
            ),
            row=1, col=3,
        )

        # Global temperature map
        fig.add_trace(
            go.Scattergeo(
                lat=current_df['lat'], lon=current_df['lon'], mode='markers+text',
                marker=dict(size=abs(current_df['temperature']) * 2, color=current_df['temperature'], 
                          colorscale='Turbo', showscale=True),
                text=current_df['city'], textposition='top center',
                hovertext=current_df.apply(lambda x: f"{x['city']}<br>{x['temperature']:.1f}°C / {x['temperature_f']:.1f}°F", axis=1),
                hoverinfo='text', name='Cities',
            ),
            row=2, col=1,
        )

        # Weather conditions pie chart
        weather_counts = current_df['weather_description'].value_counts()
        fig.add_trace(
            go.Pie(labels=weather_counts.index, values=weather_counts.values, hole=0.45, 
                  marker_colors=px.colors.qualitative.Vivid),
            row=2, col=2,
        )

        # Pressure bar chart
        fig.add_trace(
            go.Bar(x=current_df['city'], y=current_df['pressure'], marker_color='#B388FF', 
                  text=current_df['pressure'].round(0), textposition='outside'),
            row=2, col=3,
        )

        # Feels like vs actual scatter plot
        fig.add_trace(
            go.Scatter(
                x=current_df['temperature'], y=current_df['feels_like'], mode='markers+text',
                text=current_df['city'], textposition='top center',
                marker=dict(size=12, color=current_df['uv_index'], colorscale='Plasma', showscale=True),
                name='Feels like',
            ),
            row=3, col=1,
        )

        # UV Index bar chart
        fig.add_trace(
            go.Bar(x=current_df['city'], y=current_df['uv_index'], marker_color='#FFD740', 
                  text=current_df['uv_index'].round(1), textposition='outside'),
            row=3, col=2,
        )

        # Correlation heatmap
        heatmap_df = current_df[['temperature', 'humidity', 'wind_speed', 'uv_index']].corr()
        fig.add_trace(
            go.Heatmap(z=heatmap_df.values, x=heatmap_df.columns, y=heatmap_df.columns, colorscale='Viridis'),
            row=3, col=3,
        )

        fig.update_layout(
            template='plotly_dark',
            height=1450,
            title={'text': '🌈 Global Weather Intelligence Dashboard', 'x': 0.5},
            showlegend=False,
            updatemenus=[
                {
                    'type': 'buttons',
                    'direction': 'left',
                    'x': 0.12,
                    'y': 1.14,
                    'buttons': [
                        {
                            'label': 'Show °C',
                            'method': 'restyle',
                            'args': [{'y': [current_df['temperature']]}, [0]],
                        },
                        {
                            'label': 'Show °F',
                            'method': 'restyle',
                            'args': [{'y': [current_df['temperature_f']]}, [0]],
                        },
                    ],
                }
            ],
        )

        # Rotate x-axis labels
        for row, col in [(1, 1), (1, 2), (1, 3), (2, 3), (3, 2)]:
            fig.update_xaxes(tickangle=45, row=row, col=col)

        # 24h temperature trends
        trends_html = "<h2 style='text-align:center;color:#fff;margin:40px 0 15px;'>📉 24h Temperature Trends</h2>"
        if not hourly_trends_df.empty:
            trends_html += px.line(
                hourly_trends_df,
                x='forecast_time',
                y='temperature',
                color='city',
                markers=True,
                title='Last 24 Hours (All Cities)',
                template='plotly_dark',
            ).to_html(full_html=False, include_plotlyjs='cdn')

        # Build alerts
        alerts = self._build_alerts(current_df)
        alerts_html = "".join([f"<li>{a}</li>" for a in alerts]) if alerts else "<li>✅ No extreme events detected right now.</li>"

               # Statistics
        hottest = current_df.loc[current_df['temperature'].idxmax()]
        coldest = current_df.loc[current_df['temperature'].idxmin()]

        # Calculate average temperature safely
        avg_temp = hourly_trends_df['temperature'].mean() if not hourly_trends_df.empty else 0

        stats_html = f"""
        <div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin:24px 0;'>
          <div style='background:linear-gradient(135deg,#ff6ec4,#7873f5);padding:18px;border-radius:14px;color:#fff;'>
            <div>24h Average Temperature</div>
            <div style='font-size:2rem;font-weight:700;'>{avg_temp:.1f}°C</div>
          </div>
          <div style='background:linear-gradient(135deg,#00dbde,#fc00ff);padding:18px;border-radius:14px;color:#fff;'>
            <div>Hottest City</div>
            <div style='font-size:2rem;font-weight:700;'>{hottest['city']} {hottest['temperature']:.1f}°C</div>
          </div>
          <div style='background:linear-gradient(135deg,#43e97b,#38f9d7);padding:18px;border-radius:14px;color:#053;'>
            <div>Coldest City</div>
            <div style='font-size:2rem;font-weight:700;'>{coldest['city']} {coldest['temperature']:.1f}°C</div>
          </div>
        </div>
        """

        # Combine HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset='utf-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1'>
            <title>Weather Dashboard</title>
            <style>
              body {{ background: radial-gradient(circle at top,#1d2b64,#0f0c29); color:#fff; font-family:Segoe UI,Arial,sans-serif; margin:0; padding:20px; }}
              .container {{ max-width: 1850px; margin: 0 auto; }}
              .panel {{ background: rgba(255,255,255,0.06); border-radius: 16px; padding: 16px; }}
              ul {{ line-height: 1.8; }}
            </style>
        </head>
        <body>
          <div class='container'>
            <h1 style='text-align:center;font-size:3rem;margin-bottom:6px;'>🌈 Global Weather Intelligence</h1>
            <p style='text-align:center;opacity:.8;'>Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            {stats_html}
            <div class='panel'>{fig.to_html(full_html=False, include_plotlyjs='cdn')}</div>
            {trends_html}
            <div class='panel' style='margin-top:18px;'>
              <h2>🚨 Extreme Event Alerts</h2>
              <ul>{alerts_html}</ul>
            </div>
          </div>
        </body>
        </html>
        """

        # Save and open dashboard
        dashboard_path = os.path.join(tempfile.gettempdir(), 'weather_dashboard.html')
        with open(dashboard_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"{Colors.SUCCESS}✅ Dashboard created: {dashboard_path}")
        webbrowser.open('file://' + dashboard_path)
        return dashboard_path


if __name__ == '__main__':
    WeatherDashboard().create_dashboard()