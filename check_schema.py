from sqlalchemy import create_engine, text
from config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
print(f"Connecting to: {DATABASE_URL}")

with engine.connect() as conn:
    # Check if daily_forecast table exists
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='daily_forecast'"))
    table_exists = result.fetchone()
    
    if table_exists:
        print("\n✅ daily_forecast table exists")
        
        # Get column info
        result = conn.execute(text("PRAGMA table_info(daily_forecast)"))
        print("\n📋 Columns in daily_forecast:")
        print("-" * 40)
        for row in result:
            col_name = row[1]
            col_type = row[2]
            not_null = "NOT NULL" if row[3] else ""
            default = f"DEFAULT {row[4]}" if row[4] else ""
            print(f"  • {col_name:20} {col_type:10} {not_null} {default}")
    else:
        print("\n❌ daily_forecast table does NOT exist")
        
        # List all tables
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = result.fetchall()
        print("\n📋 Available tables:")
        for table in tables:
            print(f"  • {table[0]}")