import pyodbc 
import json

conn_m = pyodbc.connect('Driver={SQL Server};'
                      'Server=STARFIGHTER;'
                      'Database=analizor;'
                      'UID=phpinterface;'
                      'PWD=php')

conn_b = pyodbc.connect('Driver={SQL Server};'
                      'Server=STARFIGHTER;'
                      'Database=test_database;'
                      'UID=phpinterface;'
                      'PWD=php')

cursor_m = conn_m.cursor()
cursor_b = conn_b.cursor()
cursor_m.execute('SELECT * FROM INFORMATION_SCHEMA.TABLES')
cursor_b.execute('SELECT * FROM INFORMATION_SCHEMA.TABLES')

tables_main = []
tables_backup = []

for i in cursor_m:
    tables_main.append(i[2])

for i in cursor_b:
    tables_backup.append(i[2])

col_names = []
s=0
mapping = [("[","("),("]",")"),('"',"")]


for i in tables_main:
    if(i in tables_backup):
        cursor_m.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' ORDER BY ORDINAL_POSITION".format(i))
        for k in cursor_m:
            if(s == 0):
                col = "({}".format(k[0])
                first_table = k[0]
            else:
                col += " ,{}".format(k[0])
            s=s+1
        col += ")"
        cursor_m.execute("SELECT COUNT({}) FROM {}".format(first_table, i))
        cursor_b.execute("SELECT COUNT({}) FROM {}".format(first_table, i))
        for v in cursor_m:
            count1 = v[0]
        for v in cursor_b:
            count2 = v[0]
        if(count1 > count2):
            count = count1 - count2
            cursor_m.execute("SELECT TOP {} * FROM {} ORDER BY {} DESC".format(count, i, first_table))
            s=0
            for v in cursor_m:
                for z in v:
                    if(s == 0):
                        data = '("{}"'.format(z)
                    else:
                        data += ' ,"{}"'.format(z)
                    s=s+1
                data += ")"
                insert = "INSERT INTO {} {} VALUES {}".format(i, col, data)
                print(insert)





