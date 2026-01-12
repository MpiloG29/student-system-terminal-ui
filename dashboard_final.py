# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Student Records System - Render Deployment Version
"""

from flask import Flask, render_template_string, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Get port from environment (Render provides this)
port = int(os.environ.get("PORT", 5000))

# HTML template (same as before but shortened for this example)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Records Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 40px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }
        .stat-card { background: #667eea; color: white; padding: 20px; border-radius: 10px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Student Records Dashboard</h1>
            <p>University of Johannesburg | Deployed on Render</p>
        </div>
        {% block content %}{% endblock %}
        <div style="text-align: center; margin-top: 40px; color: #666;">
            <p>Running on Render | Port: {{ port }}</p>
        </div>
    </div>
</body>
</html>
'''

def get_db_stats():
    """Get database statistics"""
    # On Render, use absolute path
    db_path = os.path.join(os.path.dirname(__file__), 'database/student_records.db')
    
    # Create database if it doesn't exist
    if not os.path.exists(db_path):
        os.makedirs('database', exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Create basic tables
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            student_id TEXT PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            faculty TEXT,
                            year_of_study INTEGER)''')
        cursor.execute("INSERT INTO students VALUES ('UJ1001', 'John', 'Doe', 'Science', 3)")
        conn.commit()
        conn.close()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]
    except:
        total_students = 0
    
    conn.close()

    return {
        'total_students': f"{total_students:,}",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'port': port
    }

@app.route('/')
def index():
    stats = get_db_stats()
    
    content = f'''
    <div class="stats-grid">
        <div class="stat-card">
            <div>Total Students</div>
            <div style="font-size: 2em; font-weight: bold;">{stats['total_students']}</div>
            <div>Database Active</div>
        </div>
        <div class="stat-card" style="background: #4facfe;">
            <div>System Status</div>
            <div style="font-size: 2em; font-weight: bold;">✅ Live</div>
            <div>Render Deployment</div>
        </div>
    </div>
    
    <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h2>Welcome to Student System</h2>
        <p>This system is successfully deployed on Render!</p>
        <p>Database: {stats['total_students']} students loaded</p>
        <p>Time: {stats['timestamp']}</p>
    </div>
    '''
    
    return render_template_string(HTML_TEMPLATE + content, **stats)

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'student-system'}

if __name__ == '__main__':
    print(f"Starting Student Records Web Dashboard on port {port}...")
    app.run(host='0.0.0.0', port=port)
