# ��� Student Records Management System

A **colorful, terminal-based** student records management system with full CRUD operations, analytics, and beautiful visualizations.

![Terminal Dashboard](https://img.shields.io/badge/Terminal-Dashboard-blue)
![Bash](https://img.shields.io/badge/Made%20With-Bash-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)

## ✨ Features

### ��� **Beautiful Terminal UI**
- Colorful interface with emojis and visual elements
- Real-time statistics dashboard
- Progress bars and visual indicators
- Responsive design for any terminal size

### ��� **Complete Student Management**
- **Student Records**: Add, view, update, delete student information
- **Course Management**: Full course catalog with enrollment tracking
- **Grade Management**: Comprehensive grading system with GPA calculation
- **Attendance Tracking**: Daily attendance with percentage calculations
- **Enrollment System**: Course registration and status management

### ��� **Advanced Features**
- **ETL Pipeline**: Extract, Transform, Load data processing
- **Report Generation**: Multiple formats (CSV, HTML, Text)
- **Data Analytics**: Faculty performance, grade distribution, attendance trends
- **Backup System**: Automated database backups
- **Data Validation**: Input validation and error handling

## ��� Quick Start

### Prerequisites
- **Bash** (Linux/macOS/WSL)
- **SQLite3** (`sudo apt install sqlite3` or `brew install sqlite`)
- **Python3** (for data generation, optional)

### Installation
```bash
# Clone or download the project
# Make setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh#!/bin/bash

# ===================================================================
# ��� STUDENT RECORDS SYSTEM - FILE GENERATOR
# ===================================================================
# This script creates all missing files for the project
# ===================================================================

# Color definitions
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${CYAN}��� Creating Student Records System Files${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Create directory structure
mkdir -p {database,scripts,reports,logs,backups,exports,config,data}

echo -e "${GREEN}✅ Created directory structure${NC}"

# 1. Create the main application script
cat > student_system.sh << 'EOF'
#!/bin/bash
# ===================================================================
# ��� STUDENT RECORDS MANAGEMENT SYSTEM
# ===================================================================
# A colorful terminal-based student management system
# ===================================================================

# Color definitions
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m'

print_header() {
    clear
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                                                          ║${NC}"
    echo -e "${BLUE}║  ${CYAN}���  STUDENT RECORDS MANAGEMENT SYSTEM  ���            ${BLUE}║${NC}"
    echo -e "${BLUE}║  ${YELLOW}���  Terminal Dashboard with Colorful UI               ${BLUE}║${NC}"
    echo -e "${BLUE}║                                                          ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

main_menu() {
    while true; do
        print_header
        
        echo -e "${CYAN}MAIN MENU${NC}"
        echo -e "${PURPLE}══════════════════════════════════════════════${NC}"
        echo -e ""
        echo -e "  ${GREEN}1${NC}. Student Management"
        echo -e "  ${GREEN}2${NC}. Course Management"
        echo -e "  ${GREEN}3${NC}. Enrollment System"
        echo -e "  ${GREEN}4${NC}. Grade Management"
        echo -e "  ${GREEN}5${NC}. Attendance Tracking"
        echo -e "  ${GREEN}6${NC}. Reports & Analytics"
        echo -e "  ${GREEN}7${NC}. System Configuration"
        echo -e "  ${GREEN}8${NC}. Database Operations"
        echo -e "  ${GREEN}9${NC}. Visual Dashboard"
        echo -e "  ${GREEN}0${NC}. Exit System"
        echo -e ""
        echo -e "${PURPLE}══════════════════════════════════════════════${NC}"
        
        read -p "  ${YELLOW}Select option [0-9]:${NC} " choice
        
        case $choice in
            1) student_menu ;;
            2) course_menu ;;
            3) enrollment_menu ;;
            4) grade_menu ;;
            5) attendance_menu ;;
            6) reports_menu ;;
            7) config_menu ;;
            8) database_menu ;;
            9) dashboard_menu ;;
            0) exit_system ;;
            *) echo -e "${RED}Invalid option!${NC}"; sleep 1 ;;
        esac
    done
}

exit_system() {
    echo -e "\n${GREEN}Thank you for using Student Records System!${NC}"
    echo -e "${YELLOW}Goodbye! ���${NC}\n"
    exit 0
}

# Initialize the system
print_header
echo -e "${GREEN}��� Starting Student Records System...${NC}"
sleep 1
main_menu
