#!/bin/bash
clear
echo "========================================"
echo "   STUDENT RECORDS SYSTEM"
echo "   With 1000+ Students"
echo "========================================"
echo ""

# Generate CSV files if they don't exist
if [ ! -f "csv_files/students.csv" ]; then
    echo "Step 1: Generating CSV files with 1000+ students..."
    python scripts/generate_names.py
    python scripts/generate_enrollments.py
    python scripts/generate_grades.py
    python scripts/generate_attendance.py
    echo "✅ CSV files generated"
    echo ""
fi

# Load database if it doesn't exist
if [ ! -f "database/student_records.db" ]; then
    echo "Step 2: Loading data into database..."
    python scripts/load_database.py
    echo "✅ Database loaded"
    echo ""
fi

echo "Step 3: Starting the system..."
echo ""
./simple_system.sh
