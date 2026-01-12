#!/bin/bash
clear
echo "========================================"
echo "   Ìæì STUDENT RECORDS SYSTEM LAUNCHER"
echo "========================================"
echo ""
echo "Ì≥ä Available Applications:"
echo ""
echo "  1. Ì≥ù Student Records Management System"
echo "     - Manage students, courses, enrollments"
echo "     - Search, add, view records"
echo "     - Full database operations"
echo ""
echo "  2. Ìæ® Analytics Dashboard"
echo "     - Beautiful charts and visualizations"
echo "     - Real-time statistics"
echo "     - Grade distribution, faculty charts"
echo "     - Top performers, popular courses"
echo ""
echo "  3. Ì≥Å View Project Files"
echo "     - List all CSV files and database"
echo "     - Check system status"
echo ""
echo "  0. Ì∫™ Exit"
echo ""
read -p "Select application [0-3]: " choice

case $choice in
    1)
        echo ""
        echo "Starting Student Records System..."
        echo ""
        ./student_system_final.sh
        ;;
    2)
        echo ""
        echo "Starting Analytics Dashboard..."
        echo ""
        ./dashboard.sh
        ;;
    3)
        echo ""
        echo "=== PROJECT FILES ==="
        echo ""
        echo "Ì≥Å CSV Files (in csv_files/):"
        ls -lh csv_files/*.csv | awk '{print "  " $9 " - " $5 " - " $6 " " $7}'
        echo ""
        echo "Ì∑ÉÔ∏è Database:"
        if [ -f "database/student_records.db" ]; then
            size=$(du -h "database/student_records.db" | cut -f1)
            echo "  database/student_records.db - $size"
        else
            echo "  No database found"
        fi
        echo ""
        echo "Ì≥ä Scripts:"
        ls -lh *.sh | awk '{print "  " $9}'
        echo ""
        read -p "Press Enter to return to launcher..."
        ./launcher.sh
        ;;
    0)
        echo ""
        echo "Goodbye! Ì±ã"
        echo ""
        exit 0
        ;;
    *)
        echo "Invalid choice"
        sleep 1
        ./launcher.sh
        ;;
esac
