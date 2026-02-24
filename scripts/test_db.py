import sys, os, time
sys.path.insert(0, os.path.abspath('.'))
from config.settings import DATABASE_URL
from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

print('Attempting DB connection to:', DATABASE_URL)
for i in range(20):
    try:
        with engine.connect() as conn:
            r = conn.execute(text('SELECT 1'))
            print('DB connected, result:', r.scalar())
            break
    except Exception as e:
        print(f'Attempt {i+1}/20 failed: {e}')
        time.sleep(3)
else:
    print('Failed to connect to DB after retries')
    raise SystemExit(1)
