#!/bin/bash
echo "Checking database contents..."
echo ""

python3 << 'PYEOF'
import sqlite3
import os

db_path = 'database/student_records.db'
if os.path.exists(db_path):
    print(f"âœ… Database found: {db_path}")
    size = os.path.getsize(db_path) / 1024  # KB
    print(f"í³ Size: {size:.1f} KB")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print(f"\ní³Š Tables in database:")
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM "{table[0]}"')
        count = cursor.fetchone()[0]
        print(f"  â€¢ {table[0]}: {count:,} records")
    
    # Show sample data
    print(f"\ní¾“ Sample Students (first 5):")
    cursor.execute('SELECT student_id, first_name, last_name, faculty FROM students LIMIT 5')
    for row in cursor.fetchall():
        print(f"  â€¢ {row[0]}: {row[1]} {row[2]} ({row[3]})")
    
    conn.close()
else:
    print(f"âŒ Database not found at {db_path}")
PYEOF
