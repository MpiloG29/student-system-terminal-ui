#!/usr/bin/env python3
import csv
import random
from datetime import datetime, timedelta

# Read enrollments
enrollments = []
with open('csv_files/enrollments.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['status'] == 'ENROLLED':
            enrollments.append(row)

# Generate attendance records
attendance_records = []
attendance_id = 1

for enroll in enrollments[:2000]:  # Generate for first 2000 enrollments
    student_id = enroll['student_id']
    course_code = enroll['course_code']
    
    # Generate 10-15 attendance records per enrollment
    num_records = random.randint(10, 15)
    start_date = datetime(2024, 2, 1)  # Start of semester
    
    for i in range(num_records):
        attendance_date = start_date + timedelta(days=7 * i)  # Weekly classes
        
        # Determine status (mostly present)
        status = random.choices(['PRESENT', 'ABSENT', 'LATE'], weights=[0.85, 0.10, 0.05])[0]
        
        # Class duration (2-3 hours)
        total_hours = round(random.uniform(2, 3), 1)
        
        if status == 'PRESENT':
            hours_present = total_hours
        elif status == 'LATE':
            hours_present = round(total_hours * random.uniform(0.5, 0.9), 1)
        else:
            hours_present = 0
        
        attendance_records.append([
            attendance_id, student_id, course_code, attendance_date.strftime('%Y-%m-%d'),
            status, hours_present, total_hours, f"Class {i+1}"
        ])
        attendance_id += 1

# Write to CSV
with open('csv_files/attendance.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'attendance_id', 'student_id', 'course_code', 'date', 
        'status', 'hours_present', 'total_hours', 'notes'
    ])
    writer.writerows(attendance_records)

print(f"Generated {len(attendance_records)} attendance records")
print("Saved to: csv_files/attendance.csv")
