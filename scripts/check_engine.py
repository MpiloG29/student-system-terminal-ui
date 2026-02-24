import sys
import os
print('cwd:', os.getcwd())
print('sys.path[0]:', sys.path[0])
print('sys.path sample:', sys.path[:5])
try:
	from config.settings import DATABASE_URL
	print('DATABASE_URL=', DATABASE_URL)
	from sqlalchemy import create_engine
	engine = create_engine(DATABASE_URL)
	print('Engine OK')
except Exception as e:
	print('IMPORT ERROR:', repr(e))
	raise
