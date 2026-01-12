#!/usr/bin/env python3
import csv
import random
from datetime import datetime

# Read enrollments
enrollments = []
with open('csv_files/enrollments.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['status'] == 'COMPLETED':
            enrollments.append(row)

# Generate grades for completed courses
grades = []
grade_id = 1

for enroll in enrollments:
    student_id = enroll['student_id']
    course_code = enroll['course_code']
    
    # Generate assignment scores
    assignment1 = round(random.uniform(50, 100), 2)
    assignment2 = round(random.uniform(50, 100), 2)
    assignment3 = round(random.uniform(50, 100), 2)
    midterm = round(random.uniform(50, 100), 2)
    final_exam = round(random.uniform(50, 100), 2)
    
    # Calculate weighted total
    total = round(
        (assignment1 * 0.15) + 
        (assignment2 * 0.15) + 
        (assignment3 * 0.15) + 
        (midterm * 0.25) + 
        (final_exam * 0.30), 2
    )
    
    # Determine grade letter and GPA
    if total >= 75:
        grade_letter = 'A'
        gpa = 4.0
    elif total >= 70:
        grade_letter = 'B+'
        gpa = 3.5
    elif total >= 65:
        grade_letter = 'B'
        gpa = 3.0
    elif total >= 60:
        grade_letter = 'C+'
        gpa = 2.5
    elif total >= 55:
        grade_letter = 'C'
        gpa = 2.0
    elif total >= 50:
        grade_letter = 'D'
        gpa = 1.0
    else:
        grade_letter = 'F'
        gpa = 0.0
    
    # Record date
    record_date = datetime.now().strftime('%Y-%m-%d')
    
    grades.append([
        grade_id, student_id, course_code, assignment1, assignment2, assignment3,
        midterm, final_exam, total, grade_letter, gpa, '2024-1', record_date
    ])
    grade_id += 1

# Write to CSV
with open('csv_files/grades.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'grade_id', 'student_id', 'course_code', 'assignment1', 'assignment2', 'assignment3',
        'midterm', 'final_exam', 'total_score', 'grade_letter', 'gpa', 'semester', 'recorded_date'
    ])
    writer.writerows(grades)

print(f"Generated {len(grades)} grade records")
print("Saved to: csv_files/grades.csv")
