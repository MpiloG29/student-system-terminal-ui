#!/usr/bin/env python3
import csv
import random
from datetime import datetime

# Read student IDs
student_ids = []
with open('csv_files/students.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        student_ids.append(row['student_id'])

# Course codes
course_codes = []
with open('csv_files/courses.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        course_codes.append(row['course_code'])

# Generate enrollments (each student takes 4-8 courses)
enrollments = []
enrollment_id = 1
for student_id in student_ids:
    num_courses = random.randint(4, 8)
    selected_courses = random.sample(course_codes, num_courses)
    
    for course_code in selected_courses:
        # Enrollment date (within the last year)
        enroll_year = 2024
        enroll_month = random.randint(1, 12)
        enroll_day = random.randint(1, 28)
        enroll_date = f"{enroll_year}-{enroll_month:02d}-{enroll_day:02d}"
        
        # Status (mostly enrolled, some completed)
        status = random.choices(['ENROLLED', 'COMPLETED'], weights=[0.7, 0.3])[0]
        
        # Attendance (80-100% for most, some lower)
        if random.random() > 0.9:  # 10% have low attendance
            attendance = round(random.uniform(50, 79), 2)
        else:
            attendance = round(random.uniform(80, 100), 2)
        
        enrollments.append([
            enrollment_id, student_id, course_code, enroll_date, status, attendance
        ])
        enrollment_id += 1

# Write to CSV
with open('csv_files/enrollments.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['enrollment_id', 'student_id', 'course_code', 'enrollment_date', 'status', 'attendance_percentage'])
    writer.writerows(enrollments)

print(f"Generated {len(enrollments)} enrollment records")
print("Saved to: csv_files/enrollments.csv")
