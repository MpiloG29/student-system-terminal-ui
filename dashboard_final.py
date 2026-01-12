# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Web Dashboard for Student Records System
Fixed version - all SQL queries corrected
"""

from flask import Flask, render_template_string, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Records Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        .header { text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 3px solid #667eea; }
        h1 { color: #2c3e50; margin: 0; font-size: 2.5em; }
        .subtitle { color: #7f8c8d; font-size: 1.2em; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }
        .stat-card { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; transition: transform 0.3s; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-number { font-size: 2.5em; font-weight: bold; margin: 10px 0; }
        .stat-label { font-size: 1.1em; opacity: 0.9; }
        .chart-container { background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #e1e8ed; }
        .faculty-bar { height: 30px; background: #3498db; margin: 10px 0; border-radius: 5px; transition: width 0.5s; }
        .menu { display: flex; gap: 10px; margin: 30px 0; flex-wrap: wrap; }
        .menu-button { background: #3498db; color: white; border: none; padding: 12px 24px; border-radius: 25px; cursor: pointer; font-size: 1em; transition: background 0.3s; }
        .menu-button:hover { background: #2980b9; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #2c3e50; color: white; }
        tr:hover { background: #f5f5f5; }
        .search-box { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 10px; }
        input[type="text"] { padding: 10px; width: 300px; border: 2px solid #3498db; border-radius: 5px; font-size: 1em; }
        button { padding: 10px 20px; background: #2ecc71; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; }
        button:hover { background: #27ae60; }
        .footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Student Records Dashboard</h1>
            <div class="subtitle">University of Johannesburg | Students Database</div>
        </div>

        <div class="menu">
            <a href="/"><button class="menu-button">Overview</button></a>
            <a href="/students"><button class="menu-button">Students</button></a>
            <a href="/courses"><button class="menu-button">Courses</button></a>
            <a href="/faculty"><button class="menu-button">Faculty</button></a>
            <a href="/search"><button class="menu-button">Search</button></a>
        </div>

        {% block content %}{% endblock %}

        <div class="footer">
            <p>Web Dashboard | Port: 5000 | {{ timestamp }}</p>
            <p>Total Students: {{ total_students }} | Total Courses: {{ total_courses }}</p>
        </div>
    </div>
</body>
</html>
'''

def get_db_stats():
    conn = sqlite3.connect('database/student_records.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM students')
    total_students = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM courses')
    total_courses = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM enrollments')
    total_enrollments = cursor.fetchone()[0]
    conn.close()
    return {
        'total_students': f"{total_students:,}",
        'total_courses': total_courses,
        'total_enrollments': f"{total_enrollments:,}",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def index():
    stats = get_db_stats()
    
    conn = sqlite3.connect('database/student_records.db')
    cursor = conn.cursor()
    cursor.execute('SELECT faculty, COUNT(*) FROM students GROUP BY faculty ORDER BY COUNT(*) DESC')
    faculty_data = cursor.fetchall()
    
    faculty_bars = ""
    max_count = max(count for _, count in faculty_data) if faculty_data else 0
    for faculty, count in faculty_data:
        percentage = (count / int(stats['total_students'].replace(',', ''))) * 100
        bar_width = (count / max_count) * 100 if max_count > 0 else 0
        faculty_bars += f'''
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between;">
                <span>{faculty}</span>
                <span>{count:,} ({percentage:.1f}%)</span>
            </div>
            <div class="faculty-bar" style="width: {bar_width}%;"></div>
        </div>
        '''
    
    content = f'''
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">Total Students</div>
            <div class="stat-number">{stats['total_students']}</div>
            <div class="stat-label">Enrolled</div>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="stat-label">Total Courses</div>
            <div class="stat-number">{stats['total_courses']}</div>
            <div class="stat-label">Available</div>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="stat-label">Total Enrollments</div>
            <div class="stat-number">{stats['total_enrollments']}</div>
            <div class="stat-label">Registered</div>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <div class="stat-label">Database Size</div>
            <div class="stat-number">Active</div>
            <div class="stat-label">Status</div>
        </div>
    </div>

    <div class="chart-container">
        <h2>Faculty Distribution</h2>
        {faculty_bars}
    </div>

    <div class="chart-container">
        <h2>Quick Stats</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <h3>Year of Study</h3>
    '''
    
    cursor.execute('SELECT year_of_study, COUNT(*) FROM students GROUP BY year_of_study ORDER BY year_of_study')
    year_data = cursor.fetchall()
    for year, count in year_data:
        percentage = (count / int(stats['total_students'].replace(',', ''))) * 100
        content += f'<p>Year {year}: {count:,} students ({percentage:.1f}%)</p>'
    
    content += '''
            </div>
            <div>
                <h3>Student Status</h3>
    '''
    
    cursor.execute('SELECT status, COUNT(*) FROM students GROUP BY status ORDER BY COUNT(*) DESC')
    status_data = cursor.fetchall()
    for status, count in status_data:
        percentage = (count / int(stats['total_students'].replace(',', ''))) * 100
        content += f'<p>{status}: {count:,} students ({percentage:.1f}%)</p>'
    
    conn.close()
    
    content += '''
            </div>
        </div>
    </div>
    '''
    return render_template_string(HTML_TEMPLATE + content, **stats)

@app.route('/students')
def students():
    stats = get_db_stats()
    conn = sqlite3.connect('database/student_records.db')
    cursor = conn.cursor()
    cursor.execute('SELECT student_id, first_name, last_name, faculty, year_of_study, status FROM students LIMIT 50')
    students_data = cursor.fetchall()
    conn.close()
    
    table_rows = ""
    for student in students_data:
        sid, first, last, faculty, year, status = student
        table_rows += f'''
        <tr>
            <td>{sid}</td>
            <td>{first} {last}</td>
            <td>{faculty}</td>
            <td>{year}</td>
            <td>{status}</td>
        </tr>
        '''
    
    content = f'''
    <div class="chart-container">
        <h2>Student Directory (First 50)</h2>
        <table>
            <thead>
                <tr>
                    <th>Student ID</th>
                    <th>Name</th>
                    <th>Faculty</th>
                    <th>Year</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    '''
    return render_template_string(HTML_TEMPLATE + content, **stats)

@app.route('/courses')
def courses():
    stats = get_db_stats()
    conn = sqlite3.connect('database/student_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.course_code, c.course_name, c.faculty, c.instructor, 
               COUNT(e.student_id) as enrolled, c.max_capacity
        FROM courses c
        LEFT JOIN enrollments e ON c.course_code = e.course_code
        GROUP BY c.course_code
        ORDER BY c.faculty, c.course_code
    ''')
    courses_data = cursor.fetchall()
    conn.close()
    
    table_rows = ""
    for course in courses_data:
        code, name, faculty, instructor, enrolled, capacity = course
        percentage = (enrolled / capacity * 100) if capacity > 0 else 0
        status = "Low" if percentage < 70 else "Medium" if percentage < 90 else "High"
        table_rows += f'''
        <tr>
            <td>{code}</td>
            <td>{name}</td>
            <td>{faculty}</td>
            <td>{instructor}</td>
            <td>{enrolled}/{capacity}</td>
            <td>{percentage:.1f}% ({status})</td>
        </tr>
        '''
    
    content = f'''
    <div class="chart-container">
        <h2>Course Catalog</h2>
        <table>
            <thead>
                <tr>
                    <th>Course Code</th>
                    <th>Course Name</th>
                    <th>Faculty</th>
                    <th>Instructor</th>
                    <th>Enrolled/Capacity</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    '''
    return render_template_string(HTML_TEMPLATE + content, **stats)

@app.route('/faculty')
def faculty():
    stats = get_db_stats()
    conn = sqlite3.connect('database/student_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.faculty, 
               COUNT(*) as students,
               ROUND(AVG(s.year_of_study), 2) as avg_year,
               COUNT(DISTINCT c.course_code) as courses
        FROM students s
        LEFT JOIN courses c ON s.faculty = c.faculty
        GROUP BY s.faculty
        ORDER BY students DESC
    ''')
    faculty_data = cursor.fetchall()
    conn.close()
    
    table_rows = ""
    for faculty, students, avg_year, courses in faculty_data:
        percentage = (students / int(stats['total_students'].replace(',', ''))) * 100
        table_rows += f'''
        <tr>
            <td>{faculty}</td>
            <td>{students:,}</td>
            <td>{percentage:.1f}%</td>
            <td>{avg_year}</td>
            <td>{courses}</td>
        </tr>
        '''
    
    content = f'''
    <div class="chart-container">
        <h2>Faculty Analytics</h2>
        <table>
            <thead>
                <tr>
                    <th>Faculty</th>
                    <th>Students</th>
                    <th>Percentage</th>
                    <th>Avg Year</th>
                    <th>Courses</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    '''
    return render_template_string(HTML_TEMPLATE + content, **stats)

@app.route('/search', methods=['GET', 'POST'])
def search():
    stats = get_db_stats()
    content = '''
    <div class="search-box">
        <h2>Search Students</h2>
        <form method="POST">
            <input type="text" name="query" placeholder="Enter student ID, first name, or last name..." required>
            <button type="submit">Search</button>
        </form>
    </div>
    '''
    
    if request.method == 'POST':
        query = request.form['query']
        conn = sqlite3.connect('database/student_records.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT student_id, first_name, last_name, faculty, year_of_study, status, email
            FROM students 
            WHERE student_id LIKE ? OR first_name LIKE ? OR last_name LIKE ?
            LIMIT 20
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        results = cursor.fetchall()
        conn.close()
        
        if results:
            table_rows = ""
            for student in results:
                sid, first, last, faculty, year, status, email = student
                table_rows += f'''
                <tr>
                    <td>{sid}</td>
                    <td>{first} {last}</td>
                    <td>{email}</td>
                    <td>{faculty}</td>
                    <td>{year}</td>
                    <td>{status}</td>
                </tr>
                '''
            content += f'''
            <div class="chart-container">
                <h3>Search Results for "{query}" ({len(results)} found)</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Student ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Faculty</th>
                            <th>Year</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
            '''
        else:
            content += f'''
            <div class="chart-container">
                <h3>No results found for "{query}"</h3>
                <p>Try searching by student ID (e.g., UJ2024001) or name.</p>
            </div>
            '''
    
    return render_template_string(HTML_TEMPLATE + content, **stats)

if __name__ == '__main__':
    print("Starting Student Records Web Dashboard...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    if not os.path.exists('database/student_records.db'):
        print("ERROR: Database not found!")
        print("Please run the main system first to create the database.")
        exit(1)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
