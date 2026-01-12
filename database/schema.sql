-- ==================================================
-- STUDENT RECORDS DATABASE SCHEMA
-- ==================================================

-- Students Table
CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    phone VARCHAR(20),
    address TEXT,
    faculty VARCHAR(50),
    major VARCHAR(100),
    year_of_study INTEGER CHECK (year_of_study BETWEEN 1 AND 4),
    enrollment_date DATE,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    campus VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses Table
CREATE TABLE courses (
    course_code VARCHAR(20) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    faculty VARCHAR(50),
    credit_hours INTEGER DEFAULT 12,
    instructor VARCHAR(100),
    max_capacity INTEGER DEFAULT 50,
    semester VARCHAR(10),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enrollments Table
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(20) NOT NULL,
    course_code VARCHAR(20) NOT NULL,
    enrollment_date DATE,
    status VARCHAR(20) DEFAULT 'ENROLLED',
    attendance_percentage DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code),
    UNIQUE(student_id, course_code)
);

-- Grades Table
CREATE TABLE grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(20) NOT NULL,
    course_code VARCHAR(20) NOT NULL,
    assignment1 DECIMAL(5,2),
    assignment2 DECIMAL(5,2),
    assignment3 DECIMAL(5,2),
    midterm DECIMAL(5,2),
    final_exam DECIMAL(5,2),
    total_score DECIMAL(5,2),
    grade_letter VARCHAR(2),
    gpa DECIMAL(3,2),
    semester VARCHAR(10),
    recorded_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
);

-- Attendance Table
CREATE TABLE attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(20) NOT NULL,
    course_code VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'PRESENT',
    hours_present DECIMAL(4,2),
    total_hours DECIMAL(4,2),
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
);

-- Create Indexes for Performance
CREATE INDEX idx_students_faculty ON students(faculty);
CREATE INDEX idx_students_year ON students(year_of_study);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_code);
CREATE INDEX idx_grades_student ON grades(student_id);
CREATE INDEX idx_attendance_date ON attendance(date);
CREATE INDEX idx_attendance_student_course ON attendance(student_id, course_code);
