import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=STARFIGHTER;'
                      'Database=analizor;'
                      'UID=phpinterface;'
                      'PWD=php')

cursor = conn.cursor()
cursor.execute('SELECT * FROM chiller')

for i in cursor:
    print(i)
