import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=STARFIGHTER;'
                      'Database=analizor;'
                      'UID=phpinterface;'
                      'PWD=php')

cursor = conn.cursor()
cursor.execute('SELECT * FROM INFORMATION_SCHEMA.TABLES')

tables = []

for i in cursor:
    tables.append(i[2])

print(tables)
