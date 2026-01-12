#!/usr/bin/env python3
import csv
import random
from datetime import datetime, timedelta

# South African names
first_names = [
    'Lerato', 'Thando', 'Kagiso', 'Nompumelelo', 'Sipho', 'Zanele', 'Mbali', 'Tumelo', 'Naledi', 'Kgosi',
    'Amahle', 'Buhle', 'Liyana', 'Masego', 'Odwa', 'Palesa', 'Qhawe', 'Refilwe', 'Sibusiso', 'Tshepo',
    'Bongani', 'Celimpilo', 'Dumisani', 'Elias', 'Fumani', 'Gugu', 'Hlengiwe', 'Isabella', 'Jabulani', 'Khanyisile',
    'Lungile', 'Mandla', 'Nkosinathi', 'Olwethu', 'Phindile', 'Qinisela', 'Rorisang', 'Sindisiwe', 'Thabang', 'Unathi',
    'Vusumuzi', 'Wandile', 'Xolani', 'Yanga', 'Zukisa', 'Andile', 'Bhekumuzi', 'Cebo', 'Dineo', 'Elijah',
    'Fikile', 'Gabisile', 'Hlompho', 'Innocent', 'Johan', 'Kabo', 'Lucky', 'Mpho', 'Nandi', 'Omphemetse',
    'Pulane', 'Queency', 'Rebecca', 'Samkelisiwe', 'Thulisile', 'Ulandi', 'Vuyo', 'Welcome', 'Xola', 'Yolanda',
    'Zinhle', 'Anele', 'Bonga', 'Catherine', 'David', 'Enoch', 'Faith', 'Grace', 'Hope', 'Isaiah',
    'James', 'Kelly', 'Leroy', 'Michael', 'Nathan', 'Olivia', 'Peter', 'Queen', 'Robert', 'Sarah',
    'Thomas', 'Ursula', 'Victor', 'William', 'Xavier', 'Yvonne', 'Zachariah', 'Abigail', 'Benjamin', 'Christopher'
]

last_names = [
    'Mkhize', 'Ndlovu', 'Botha', 'Van der Merwe', 'Smith', 'Petersen', 'Williams', 'Jones', 'Brown', 'Davis',
    'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin',
    'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall',
    'Allen', 'Young', 'Hernandez', 'King', 'Wright', 'Lopez', 'Hill', 'Scott', 'Green', 'Adams',
    'Baker', 'Gonzalez', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner', 'Phillips', 'Campbell',
    'Parker', 'Evans', 'Edwards', 'Collins', 'Stewart', 'Sanchez', 'Morris', 'Rogers', 'Reed', 'Cook',
    'Morgan', 'Bell', 'Murphy', 'Bailey', 'Rivera', 'Cooper', 'Richardson', 'Cox', 'Howard', 'Ward',
    'Torres', 'Peterson', 'Gray', 'Ramirez', 'James', 'Watson', 'Brooks', 'Kelly', 'Sanders', 'Price',
    'Bennett', 'Wood', 'Barnes', 'Ross', 'Henderson', 'Coleman', 'Jenkins', 'Perry', 'Powell', 'Long',
    'Patterson', 'Hughes', 'Flores', 'Washington', 'Butler', 'Simmons', 'Foster', 'Gonzales', 'Bryant', 'Alexander'
]

faculties = ['FEBE', 'FHES', 'FADA', 'FCBE', 'FEDU', 'FHSS', 'FLM', 'FMS', 'FNS']
majors = {
    'FEBE': ['Computer Engineering', 'Electrical Engineering', 'Civil Engineering', 'Mechanical Engineering', 'Chemical Engineering'],
    'FHES': ['Medical Science', 'Pharmacy', 'Nursing', 'Physiotherapy', 'Dentistry'],
    'FADA': ['Architecture', 'Fine Arts', 'Graphic Design', 'Urban Planning', 'Interior Design'],
    'FCBE': ['Business Administration', 'Accounting', 'Finance', 'Marketing', 'Economics'],
    'FEDU': ['Education', 'Early Childhood Development', 'Special Needs Education', 'Curriculum Studies'],
    'FHSS': ['Sociology', 'Psychology', 'Political Science', 'Anthropology', 'Social Work'],
    'FLM': ['Law', 'Criminology', 'Forensic Science', 'Legal Studies'],
    'FMS': ['Medical Science', 'Biochemistry', 'Microbiology', 'Genetics'],
    'FNS': ['Nursing', 'Midwifery', 'Public Health', 'Health Administration']
}

campuses = ['APK', 'APB', 'DFC', 'SWC']

# Generate 1000 students
students_data = []
for i in range(1, 1001):
    first = random.choice(first_names)
    last = random.choice(last_names)
    faculty = random.choice(faculties)
    major = random.choice(majors[faculty])
    year = random.randint(1, 4)
    campus = random.choice(campuses)
    student_id = f'UJ2024{str(i).zfill(3)}'
    email = f"{first.lower()}.{last.lower()}@student.uj.ac.za"
    
    # Generate birth date (18-25 years old)
    birth_year = 2024 - random.randint(18, 25)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    dob = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
    
    # Enrollment date (within last 1-4 years)
    enroll_year = 2024 - random.randint(1, 4)
    enroll_month = random.randint(1, 12)
    enroll_day = random.randint(1, 28)
    enroll_date = f"{enroll_year}-{enroll_month:02d}-{enroll_day:02d}"
    
    # Status (mostly active, some graduated/suspended)
    if year == 4 and random.random() > 0.7:
        status = 'GRADUATED'
    elif random.random() > 0.95:
        status = 'SUSPENDED'
    else:
        status = 'ACTIVE'
    
    students_data.append([
        student_id, first, last, email, dob, f"27{random.randint(10000000, 99999999)}",
        f"{random.randint(1, 999)} Street, {campus} Campus", faculty, major, year,
        enroll_date, status, campus
    ])

# Write to CSV
with open('csv_files/students.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone', 
                     'address', 'faculty', 'major', 'year_of_study', 'enrollment_date', 'status', 'campus'])
    writer.writerows(students_data)

print(f"Generated {len(students_data)} student records")
print("Saved to: csv_files/students.csv")
