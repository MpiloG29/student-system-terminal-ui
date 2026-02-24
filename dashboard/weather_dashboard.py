import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine, text
import webbrowser
import tempfile
import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import Colors, DATABASE_URL

class WeatherDashboard:
    """Create interactive dashboard from weather data"""
    
    def __init__(self):
        # Use the same SQLite database as the ETL pipeline
        self.connection_string = DATABASE_URL
        self.engine = create_engine(self.connection_string)
        
    def get_current_weather(self):
        """Get latest current weather for all locations"""
        query = text("""
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
                SELECT MAX(recorded_at) 
                FROM current_weather cw2 
                WHERE cw2.location_id = cw.location_id
            )
            ORDER BY cw.temperature DESC
        """)
        
        return pd.read_sql(query, self.engine)
    
    def get_weekly_forecast(self, city):
        """Get weekly forecast for a specific city - UPDATED to match actual schema"""
        query = text("""
            SELECT 
                df.forecast_date,
                df.temperature_max,
                df.temperature_min,
                df.precipitation_probability_max as precipitation_prob,
                df.wind_speed_max as wind_speed
            FROM daily_forecast df
            JOIN locations l ON df.location_id = l.location_id
            WHERE l.city = :city
            ORDER BY df.forecast_date
            LIMIT 7
        """)
        
        return pd.read_sql(query, self.engine, params={"city": city})
    
    def create_dashboard(self):
        """Create interactive HTML dashboard"""
        
        print(f"{Colors.INFO}📊 Creating weather dashboard...")
        
        # Get data
        current_df = self.get_current_weather()
        
        if current_df.empty:
            print(f"{Colors.ERROR}❌ No data available. Please run the pipeline first.")
            return None
        
        # City coordinates for map (approximate)
        city_coords = {
            'New York': {'lat': 40.7128, 'lon': -74.0060},
            'London': {'lat': 51.5074, 'lon': -0.1278},
            'Tokyo': {'lat': 35.6762, 'lon': 139.6503},
            'Sydney': {'lat': -33.8688, 'lon': 151.2093},
            'Rio de Janeiro': {'lat': -22.9068, 'lon': -43.1729},
            'Cape Town': {'lat': -33.9249, 'lon': 18.4241},
            'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
            'Dubai': {'lat': 25.2048, 'lon': 55.2708}
        }
        
        # Add coordinates to dataframe
        current_df['lat'] = current_df['city'].map(lambda x: city_coords.get(x, {}).get('lat', 0))
        current_df['lon'] = current_df['city'].map(lambda x: city_coords.get(x, {}).get('lon', 0))
        
        # Create main dashboard figure with subplots
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=('🌡️ Current Temperatures', '💧 Humidity Levels', 
                          '🌪️ Wind Speed', '☀️ UV Index', 
                          '📍 Global Temperature Map', '📊 Temperature Distribution',
                          '🔥 Feels Like vs Actual', '📈 Pressure Levels', '🌍 Weather Conditions'),
            specs=[
                [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
                [{'type': 'scattergeo'}, {'type': 'pie'}, {'type': 'scatter'}],
                [{'type': 'bar'}, {'type': 'bar'}, {'type': 'domain'}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Temperature bar chart
        colors_temp = ['red' if t > 25 else 'orange' if t > 15 else 'blue' for t in current_df['temperature']]
        fig.add_trace(
            go.Bar(x=current_df['city'], y=current_df['temperature'],
                  name='Temperature (°C)', marker_color=colors_temp,
                  text=current_df['temperature'].round(1),
                  textposition='outside'),
            row=1, col=1
        )
        
        # 2. Humidity bar chart
        colors_humidity = ['darkblue' if h > 70 else 'lightblue' for h in current_df['humidity']]
        fig.add_trace(
            go.Bar(x=current_df['city'], y=current_df['humidity'],
                  name='Humidity (%)', marker_color=colors_humidity,
                  text=current_df['humidity'].round(0),
                  textposition='outside'),
            row=1, col=2
        )
        
        # 3. Wind speed bar chart
        colors_wind = ['darkgreen' if w > 20 else 'lightgreen' for w in current_df['wind_speed']]
        fig.add_trace(
            go.Bar(x=current_df['city'], y=current_df['wind_speed'],
                  name='Wind Speed (km/h)', marker_color=colors_wind,
                  text=current_df['wind_speed'].round(1),
                  textposition='outside'),
            row=1, col=3
        )
        
        # 4. Global temperature map - FIXED: Use abs() for marker size
        fig.add_trace(
            go.Scattergeo(
                lat=current_df['lat'],
                lon=current_df['lon'],
                mode='markers+text',
                marker=dict(
                    size=abs(current_df['temperature']) * 2,
                    color=current_df['temperature'],
                    colorscale='RdYlGn_r',
                    showscale=True,
                    colorbar=dict(title="Temperature °C")
                ),
                text=current_df['city'],
                textposition="top center",
                name='Cities',
                hoverinfo='text',
                hovertext=current_df.apply(
                    lambda x: f"{x['city']}: {x['temperature']}°C, {x['weather_description']}", 
                    axis=1
                )
            ),
            row=2, col=1
        )
        
        # 5. Temperature distribution pie chart
        temp_ranges = pd.cut(current_df['temperature'], 
                            bins=[-50, 0, 10, 20, 30, 50],
                            labels=['<0°C', '0-10°C', '10-20°C', '20-30°C', '>30°C'])
        temp_dist = temp_ranges.value_counts()
        fig.add_trace(
            go.Pie(labels=temp_dist.index, values=temp_dist.values,
                  name='Temperature Distribution',
                  marker_colors=['darkblue', 'blue', 'lightgreen', 'orange', 'red']),
            row=2, col=2
        )
        
        # 6. Feels like vs actual scatter plot
        fig.add_trace(
            go.Scatter(x=current_df['temperature'], y=current_df['feels_like'],
                      mode='markers+text',
                      marker=dict(size=12, color=current_df['uv_index'],
                                colorscale='Viridis', showscale=True,
                                colorbar=dict(title="UV Index")),
                      text=current_df['city'],
                      textposition="top center",
                      name='Feels Like vs Actual'),
            row=2, col=3
        )
        
        # Add diagonal line for reference
        fig.add_trace(
            go.Scatter(x=[0, 40], y=[0, 40],
                      mode='lines',
                      line=dict(dash='dash', color='gray'),
                      showlegend=False),
            row=2, col=3
        )
        
        # 7. Pressure bar chart
        fig.add_trace(
            go.Bar(x=current_df['city'], y=current_df['pressure'],
                  name='Pressure (hPa)', marker_color='purple',
                  text=current_df['pressure'].round(0),
                  textposition='outside'),
            row=3, col=1
        )
        
        # 8. UV Index bar chart
        colors_uv = ['darkred' if uv > 7 else 'orange' if uv > 3 else 'yellow' for uv in current_df['uv_index']]
        fig.add_trace(
            go.Bar(x=current_df['city'], y=current_df['uv_index'],
                  name='UV Index', marker_color=colors_uv,
                  text=current_df['uv_index'].round(1),
                  textposition='outside'),
            row=3, col=2
        )
        
        # 9. Weather conditions donut chart
        weather_counts = current_df['weather_description'].value_counts()
        fig.add_trace(
            go.Pie(labels=weather_counts.index, values=weather_counts.values,
                  hole=0.4, name='Weather Conditions',
                  marker_colors=px.colors.qualitative.Set3),
            row=3, col=3
        )
        
        # Update layout
        fig.update_layout(
            title={
                'text': "🌍 Global Weather Dashboard",
                'y':0.98,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=24, family="Arial Black")
            },
            showlegend=False,
            height=1400,
            template='plotly_dark',
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                countrycolor='rgb(204, 204, 204)'
            )
        )
        
        # Update axes
        fig.update_xaxes(tickangle=45, row=1, col=1)
        fig.update_xaxes(tickangle=45, row=1, col=2)
        fig.update_xaxes(tickangle=45, row=1, col=3)
        fig.update_xaxes(tickangle=45, row=3, col=1)
        fig.update_xaxes(tickangle=45, row=3, col=2)
        
        # Create weekly forecasts section - UPDATED to match new query
        forecast_html = "<h2 style='color: white; text-align: center; margin: 40px 0 20px;'>📅 7-Day Forecasts</h2>"
        forecast_html += "<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;'>"
        
        for city in current_df['city'].head(4):
            forecast_df = self.get_weekly_forecast(city)
            if not forecast_df.empty:
                fig_forecast = go.Figure()
                
                fig_forecast.add_trace(go.Scatter(
                    x=forecast_df['forecast_date'],
                    y=forecast_df['temperature_max'],
                    name='Max Temp',
                    line=dict(color='red', width=3),
                    mode='lines+markers',
                    marker=dict(size=8)
                ))
                
                fig_forecast.add_trace(go.Scatter(
                    x=forecast_df['forecast_date'],
                    y=forecast_df['temperature_min'],
                    name='Min Temp',
                    line=dict(color='blue', width=3),
                    mode='lines+markers',
                    marker=dict(size=8)
                ))
                
                fig_forecast.add_trace(go.Bar(
                    x=forecast_df['forecast_date'],
                    y=forecast_df['precipitation_prob'],
                    name='Precipitation %',
                    yaxis='y2',
                    marker_color='lightblue',
                    opacity=0.5
                ))
                
                fig_forecast.update_layout(
                    title=f"{city} - Weekly Forecast",
                    xaxis_title="Date",
                    yaxis_title="Temperature (°C)",
                    yaxis2=dict(
                        title="Precipitation %",
                        overlaying='y',
                        side='right',
                        range=[0, 100]
                    ),
                    template='plotly_dark',
                    height=350,
                    margin=dict(l=50, r=50, t=50, b=50),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                forecast_html += f"<div style='background: #1f1f1f; border-radius: 10px; padding: 15px;'>{fig_forecast.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
        
        forecast_html += "</div>"
        
        # Create statistics cards
        hottest_idx = current_df['temperature'].idxmax()
        coldest_idx = current_df['temperature'].idxmin()
        
        stats_html = f"""
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0;'>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; padding: 20px; color: white; text-align: center;'>
                <div style='font-size: 1.2em; opacity: 0.9;'>Cities Tracked</div>
                <div style='font-size: 3em; font-weight: bold;'>{len(current_df)}</div>
            </div>
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; padding: 20px; color: white; text-align: center;'>
                <div style='font-size: 1.2em; opacity: 0.9;'>Hottest City</div>
                <div style='font-size: 2em; font-weight: bold;'>{current_df.loc[hottest_idx, 'city']}</div>
                <div style='font-size: 1.5em;'>{current_df.loc[hottest_idx, 'temperature']:.1f}°C</div>
            </div>
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 15px; padding: 20px; color: white; text-align: center;'>
                <div style='font-size: 1.2em; opacity: 0.9;'>Coldest City</div>
                <div style='font-size: 2em; font-weight: bold;'>{current_df.loc[coldest_idx, 'city']}</div>
                <div style='font-size: 1.5em;'>{current_df.loc[coldest_idx, 'temperature']:.1f}°C</div>
            </div>
            <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 15px; padding: 20px; color: white; text-align: center;'>
                <div style='font-size: 1.2em; opacity: 0.9;'>Average Humidity</div>
                <div style='font-size: 2.5em; font-weight: bold;'>{current_df['humidity'].mean():.0f}%</div>
            </div>
        </div>
        """
        
        # Combine everything into final HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Global Weather Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    color: white;
                }}
                .dashboard-container {{
                    max-width: 1800px;
                    margin: 0 auto;
                }}
                h1 {{
                    text-align: center;
                    font-size: 3.5em;
                    margin-bottom: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                .timestamp {{
                    text-align: center;
                    color: #888;
                    margin-bottom: 30px;
                    font-size: 1.1em;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 50px;
                    padding: 20px;
                    color: #666;
                    border-top: 1px solid #333;
                }}
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <h1>☀️ Global Weather Dashboard 🌧️</h1>
                <div class="timestamp">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                
                {stats_html}
                
                <div style='background: rgba(255,255,255,0.05); border-radius: 20px; padding: 20px; margin: 30px 0;'>
                    {fig.to_html(full_html=False, include_plotlyjs='cdn')}
                </div>
                
                {forecast_html}
                
                <div class="footer">
                    🌟 Weather Data Pipeline Portfolio Project | Built with Python, SQLite, and Plotly
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save to file
        dashboard_path = os.path.join(tempfile.gettempdir(), 'weather_dashboard.html')
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"{Colors.SUCCESS}✅ Dashboard created: {dashboard_path}")
        webbrowser.open('file://' + dashboard_path)
        
        return dashboard_path

if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.create_dashboard()