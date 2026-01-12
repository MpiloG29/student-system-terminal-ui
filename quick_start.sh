#!/bin/bash
echo "========================================"
echo "   QUICK START: STUDENT RECORDS SYSTEM"
echo "========================================"
echo ""

echo "Ì≥ä Generating CSV files with 1000+ students..."
python scripts/generate_names.py
python scripts/generate_enrollments.py
python scripts/generate_grades.py
python scripts/generate_attendance.py

echo ""
echo "Ì∑ÉÔ∏è  Loading data into database..."
python scripts/load_database.py

echo ""
echo "Ì∫Ä Starting Student Records System..."
echo ""
./student_records_system.sh
