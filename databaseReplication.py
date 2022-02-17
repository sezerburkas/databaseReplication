import pyodbc 
import json
from alive_progress import alive_bar
import time

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

print("Tables are scanning...")
for i in tables_main:
    if(i in tables_backup):
        data_type = []
        s=0
        cursor_m.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' ORDER BY ORDINAL_POSITION".format(i))
        for k in cursor_m:
            if(s == 0):
                first_table = k[0]
                col = "({}".format(k[0])
            else:
                col += " ,{}".format(k[0])
            data_type.append(k[1])
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
            print("{} changes detected for table {}".format(count, i))
            cursor_m.execute("SELECT TOP {} * FROM {} ORDER BY {} DESC".format(count, i, first_table))
            with alive_bar(count) as bar:
                for v in cursor_m:
                    s=0
                    for z in v:
                        if(z == None):
                            val = ""
                        else:
                            val = z
                        if(s == 0):
                            data = "('{}'".format(val)
                        else:
                            if(data_type[s] == "datetime" or data_type[s] == "date"):
                                data += ", CAST('{}' as datetime2)".format(val)
                            else:
                                if(isinstance(val, str)):
                                    quote = val.find("'")
                                    if(quote != -1):
                                        val = "{}'{}".format(val[:quote],val[quote:-1])
                                data += ", '{}'".format(val)
                        s=s+1
                    data += ")"
                    insert = "INSERT INTO {} {} VALUES {}".format(i, col, data)
                    try:
                        cursor_b.execute(insert)
                        conn_b.commit()
                    except:
                        print(insert)
                    bar()
    else:
        print("{} is not exist!".format(i))
                



