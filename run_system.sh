#!/bin/bash
clear
echo "========================================"
echo "   STUDENT RECORDS MANAGEMENT SYSTEM"
echo "   With 1000+ Students Database"
echo "========================================"
echo ""

# Check if we have all CSV files
echo "Checking CSV files..."
if [ ! -f "csv_files/students.csv" ]; then
    echo "ERROR: students.csv not found!"
    exit 1
fi

if [ ! -f "csv_files/courses.csv" ]; then
    echo "ERROR: courses.csv not found!"
    exit 1
fi

if [ ! -f "csv_files/enrollments.csv" ]; then
    echo "ERROR: enrollments.csv not found!"
    exit 1
fi

if [ ! -f "csv_files/grades.csv" ]; then
    echo "Generating grades.csv..."
    python scripts/generate_grades.py
fi

if [ ! -f "csv_files/attendance.csv" ]; then
    echo "Generating attendance.csv..."
    python scripts/generate_attendance.py
fi

# Check if database exists
if [ ! -f "database/student_records.db" ]; then
    echo "Creating database..."
    python scripts/load_database_clean.py
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create database"
        exit 1
    fi
    echo ""
fi

# Show menu
while true; do
    echo "=== MAIN MENU ==="
    echo "1. View Database Statistics"
    echo "2. View Students (sample)"
    echo "3. View Courses"
    echo "4. Search Student"
    echo "5. List CSV Files"
    echo "6. Test Database Connection"
    echo "0. Exit"
    echo ""
    read -p "Select option: " choice
    
    case $choice in
        1)
            echo ""
            echo "=== DATABASE STATISTICS ==="
            python3 -c "
import sqlite3
conn = sqlite3.connect('database/student_records.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM students')
students = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM courses')
courses = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM enrollments')
enrollments = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM grades')
grades = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM attendance')
attendance = cursor.fetchone()[0]

print(f'Total Students: {students:,}')
print(f'Total Courses: {courses}')
print(f'Total Enrollments: {enrollments:,}')
print(f'Grade Records: {grades:,}')
print(f'Attendance Records: {attendance:,}')

print()
print('Faculty Distribution:')
cursor.execute('SELECT faculty, COUNT(*) FROM students GROUP BY faculty ORDER BY COUNT(*) DESC')
for faculty, count in cursor.fetchall():
    print(f'  {faculty}: {count} students')

conn.close()
"
            echo ""
            read -p "Press Enter to continue..."
            ;;
        2)
            echo ""
            echo "=== STUDENT SAMPLE (First 10) ==="
            python3 -c "
import sqlite3
conn = sqlite3.connect('database/student_records.db')
cursor = conn.cursor()

cursor.execute('SELECT student_id, first_name, last_name, faculty, year_of_study FROM students LIMIT 10')

print('ID          Name                  Faculty Year')
print('----------  --------------------  ------- ----')
for row in cursor.fetchall():
    sid, first, last, faculty, year = row
    name = f'{first} {last}'
    print(f'{sid:10}  {name:20}  {faculty:7}  {year:4}')

conn.close()
"
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            echo ""
            echo "=== COURSES ==="
            python3 -c "
import sqlite3
conn = sqlite3.connect('database/student_records.db')
cursor = conn.cursor()

cursor.execute('SELECT course_code, course_name, faculty, instructor FROM courses ORDER BY faculty, course_code')

print('Code      Course                Faculty Instructor')
print('--------  --------------------  ------- ---------------')
for row in cursor.fetchall():
    code, name, faculty, instructor = row
    print(f'{code:8}  {name:20}  {faculty:7}  {instructor:15}')

conn.close()
"
            echo ""
            read -p "Press Enter to continue..."
            ;;
        4)
            echo ""
            echo "=== SEARCH STUDENT ==="
            read -p "Enter student ID or name: " search
            python3 << PYEOF
import sqlite3
conn = sqlite3.connect('database/student_records.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT student_id, first_name, last_name, faculty, major, year_of_study
    FROM students 
    WHERE student_id LIKE ? OR first_name LIKE ? OR last_name LIKE ?
    LIMIT 5
''', (f'%{search}%', f'%{search}%', f'%{search}%'))

results = cursor.fetchall()
if results:
    print(f'Found {len(results)} student(s):')
    for row in results:
        sid, first, last, faculty, major, year = row
        print(f'  {sid}: {first} {last} ({faculty}, Year {year})')
else:
    print(f'No students found matching: {search}')

conn.close()
PYEOF
            echo ""
            read -p "Press Enter to continue..."
            ;;
        5)
            echo ""
            echo "=== CSV FILES ==="
            echo "File                  Records"
            echo "------------------  ---------"
            for file in csv_files/*.csv; do
                if [ -f "$file" ]; then
                    count=$(tail -n +2 "$file" 2>/dev/null | wc -l)
                    filename=$(basename "$file")
                    echo "$filename  $count"
                fi
            done
            echo ""
            echo "students.csv sample:"
            head -3 csv_files/students.csv | column -t -s,
            echo ""
            read -p "Press Enter to continue..."
            ;;
        6)
            echo ""
            echo "=== DATABASE TEST ==="
            if [ -f "database/student_records.db" ]; then
                size=$(du -h "database/student_records.db" | cut -f1)
                echo "Database: database/student_records.db"
                echo "Size: $size"
                
                python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('database/student_records.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
    tables = cursor.fetchall()
    print(f'Tables: {len(tables)}')
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM \"{table[0]}\"')
        count = cursor.fetchone()[0]
        print(f'  {table[0]}: {count:,} records')
    conn.close()
    print('Database connection: OK')
except Exception as e:
    print(f'Error: {e}')
"
            else
                echo "Database file not found!"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        0)
            echo ""
            echo "Goodbye!"
            echo ""
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            sleep 1
            ;;
    esac
    
    echo ""
done
