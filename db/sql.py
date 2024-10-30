import mysql.connector as sql
import pandas as pd

#crear la cadena del conector
connector = sql.connect(host="localhost", user="root", password="", database="arpa")

if connector.is_connected():
    print('Well done')
    #perform db operations
else:
    print('Try again')
    
connector.close()
    
    