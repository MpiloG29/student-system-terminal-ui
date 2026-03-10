from flask import Flask, send_file, render_template_string
import subprocess
import os
import threading
from datetime import datetime
import tempfile
import time

app = Flask(__name__)

# HTML template for the home page
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Data Pipeline</title>
    <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            max-width: 1200px; 
            margin: 0 auto; 
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
        }
        .container {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        h1 { font-size: 3em; margin-bottom: 20px; }
        .button { 
            display: inline-block; 
            padding: 15px 30px; 
            margin: 10px; 
            background: white; 
            color: #667eea;
            text-decoration: none; 
            border-radius: 50px;
            font-weight: bold;
            transition: transform 0.3s;
            border: none;
            cursor: pointer;
            font-size: 1.1em;
        }
        .button:hover { transform: scale(1.05); }
        .status { 
            margin: 30px 0; 
            padding: 20px; 
            background: rgba(255,255,255,0.2); 
            border-radius: 10px;
            text-align: left;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat-card {
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 10px;
        }
        .stat-value { font-size: 2em; font-weight: bold; }
        .stat-label { font-size: 0.9em; opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather Data Pipeline</h1>
        <p>Real-time weather data for 8 global cities</p>
        
        <div>
            <a href="/dashboard" class="button">📊 View Live Dashboard</a>
            <a href="/run-pipeline" class="button">🚀 Refresh Weather Data</a>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">8</div>
                <div class="stat-label">Cities Tracked</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="last-run">Loading...</div>
                <div class="stat-label">Last Run</div>
            </div>
        </div>
        
        <div class="status" id="status">
            <h3>System Status: <span id="system-status">✅ Running</span></h3>
        </div>
    </div>

    <script>
        function updateStatus() {
            fetch('/status').then(r => r.json()).then(data => {
                document.getElementById('last-run').textContent = data.last_run || 'Never';
                document.getElementById('system-status').textContent = data.is_running ? '🔄 Running' : '✅ Idle';
            });
        }
        updateStatus();
        setInterval(updateStatus, 5000);
    </script>
</body>
</html>
"""

# Store pipeline state
pipeline_state = {
    'last_run': None,
    'is_running': False
}

@app.route('/')
def home():
    return render_template_string(HOME_HTML)

@app.route('/status')
def status():
    return {'last_run': pipeline_state['last_run'], 'is_running': pipeline_state['is_running']}

@app.route('/run-pipeline')
def run_pipeline():
    if pipeline_state['is_running']:
        return "Pipeline already running", 429
    
    def run():
        pipeline_state['is_running'] = True
        try:
            result = subprocess.run(['python', 'run_pipeline.py', '1'], 
                                  capture_output=True, text=True, timeout=60)
            pipeline_state['last_run'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Pipeline output: {result.stdout}")
        except Exception as e:
            print(f"Error running pipeline: {e}")
        finally:
            pipeline_state['is_running'] = False
    
    threading.Thread(target=run).start()
    return "Pipeline started! Check back in a minute."

@app.route('/dashboard')
def dashboard():
    try:
        # Generate fresh dashboard
        result = subprocess.run(['python', 'run_pipeline.py', '2'], 
                              capture_output=True, text=True, timeout=30)
        
        # Find the dashboard file
        dashboard_path = os.path.join(tempfile.gettempdir(), 'weather_dashboard.html')
        
        if os.path.exists(dashboard_path):
            return send_file(dashboard_path)
        else:
            return "Dashboard not found. Run the pipeline first.", 404
    except Exception as e:
        return f"Error generating dashboard: {str(e)}", 500

# Run the pipeline once at startup (optional)
def run_startup_pipeline():
    time.sleep(5)  # Wait for server to start
    pipeline_state['is_running'] = True
    try:
        subprocess.run(['python', 'run_pipeline.py', '1'], timeout=60)
        pipeline_state['last_run'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass
    finally:
        pipeline_state['is_running'] = False

if __name__ == '__main__':
    # Start background thread for initial pipeline run
    threading.Thread(target=run_startup_pipeline, daemon=True).start()
    
    # Start web server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)