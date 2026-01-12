#!/usr/bin/env python3
import sqlite3
import csv
import os
from datetime import datetime

print("=" * 60)
print("LOADING STUDENT RECORDS DATABASE")
print("=" * 60)

# Create database directory
os.makedirs('database', exist_ok=True)

# Connect to database
conn = sqlite3.connect('database/student_records.db')
cursor = conn.cursor()

print("Ì≥ä Creating tables from schema...")
with open('database/schema.sql', 'r', encoding='utf-8') as f:
    schema = f.read()
    cursor.executescript(schema)

print("‚úÖ Tables created successfully")

# Load students
print("\nÌ±• Loading students data...")
with open('csv_files/students.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    students = []
    for row in reader:
        students.append((
            row['student_id'], row['first_name'], row['last_name'],
            row['email'], row['date_of_birth'], row['phone'], row['address'],
            row['faculty'], row['major'], int(row['year_of_study']),
            row['enrollment_date'], row['status'], row['campus']
        ))

cursor.executemany('''
    INSERT OR IGNORE INTO students 
    (student_id, first_name, last_name, email, date_of_birth, phone, address,
     faculty, major, year_of_study, enrollment_date, status, campus)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', students)
print(f"‚úÖ Loaded {len(students)} students")

# Load courses
print("\nÌ≥ö Loading courses data...")
with open('csv_files/courses.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    courses = []
    for row in reader:
        courses.append((
            row['course_code'], row['course_name'], row['faculty'],
            int(row['credit_hours']), row['instructor'],
            int(row['max_capacity']), row['semester'], row['description']
        ))

cursor.executemany('''
    INSERT OR IGNORE INTO courses 
    (course_code, course_name, faculty, credit_hours, instructor, 
     max_capacity, semester, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', courses)
print(f"‚úÖ Loaded {len(courses)} courses")

# Load enrollments
print("\nÌ≥ù Loading enrollments data...")
with open('csv_files/enrollments.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    enrollments = []
    for row in reader:
        enrollments.append((
            int(row['enrollment_id']), row['student_id'], row['course_code'],
            row['enrollment_date'], row['status'], float(row['attendance_percentage'])
        ))

cursor.executemany('''
    INSERT OR IGNORE INTO enrollments 
    (enrollment_id, student_id, course_code, enrollment_date, status, attendance_percentage)
    VALUES (?, ?, ?, ?, ?, ?)
''', enrollments)
print(f"‚úÖ Loaded {len(enrollments)} enrollments")

# Load grades
print("\nÌ≥à Loading grades data...")
with open('csv_files/grades.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    grades = []
    for row in reader:
        grades.append((
            int(row['grade_id']), row['student_id'], row['course_code'],
            float(row['assignment1']), float(row['assignment2']), float(row['assignment3']),
            float(row['midterm']), float(row['final_exam']), float(row['total_score']),
            row['grade_letter'], float(row['gpa']), row['semester'], row['recorded_date']
        ))

cursor.executemany('''
    INSERT OR IGNORE INTO grades 
    (grade_id, student_id, course_code, assignment1, assignment2, assignment3,
     midterm, final_exam, total_score, grade_letter, gpa, semester, recorded_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', grades)
print(f"‚úÖ Loaded {len(grades)} grade records")

# Load attendance
print("\nÌ≥Ö Loading attendance data...")
with open('csv_files/attendance.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    attendance = []
    for row in reader:
        attendance.append((
            int(row['attendance_id']), row['student_id'], row['course_code'],
            row['date'], row['status'], float(row['hours_present']),
            float(row['total_hours']), row['notes']
        ))

cursor.executemany('''
    INSERT OR IGNORE INTO attendance 
    (attendance_id, student_id, course_code, date, status, hours_present, total_hours, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', attendance)
print(f"‚úÖ Loaded {len(attendance)} attendance records")

# Commit and close
conn.commit()
conn.close()

print("\n" + "=" * 60)
print("‚úÖ DATABASE LOAD COMPLETE!")
print("=" * 60)
print(f"\nÌ≥ä Database Statistics:")
print(f"   ‚Ä¢ Students: {len(students)}")
print(f"   ‚Ä¢ Courses: {len(courses)}")
print(f"   ‚Ä¢ Enrollments: {len(enrollments)}")
print(f"   ‚Ä¢ Grade Records: {len(grades)}")
print(f"   ‚Ä¢ Attendance Records: {len(attendance)}")
print(f"\nÌ≥Å Database saved to: database/student_records.db")
print(f"Ì≥Å CSV files in: csv_files/")
