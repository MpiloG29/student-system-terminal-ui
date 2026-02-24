import config.settings as s
print('module file:', s.__file__)
print('type:', type(s.DATABASE_URL))
print('repr:', repr(s.DATABASE_URL))
print('raw:', s.DATABASE_URL)
