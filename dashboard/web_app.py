from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Weather Data Pipeline</h1>
    <a href="/run">Run Pipeline</a> | <a href="/dashboard">View Dashboard</a>
    '''

@app.route('/run')
def run_pipeline():
    result = subprocess.run(['python', 'run_pipeline.py', '1'], 
                          capture_output=True, text=True)
    return f"<pre>{result.stdout}</pre>"

@app.route('/dashboard')
def dashboard():
    # Generate and serve dashboard
    subprocess.run(['python', 'run_pipeline.py', '2'])
    return send_file('/tmp/weather_dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)