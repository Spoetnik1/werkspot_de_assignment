import mysql.connector
from mysql.connector import errorcode

#mysql.connector for running direct SQL querries.
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="root")
mycursor = mydb.cursor()

with open('create_tables_scheme_query.sql', 'r') as file:
  schema_table_query = file.read()

mycursor.execute(schema_table_query, multi=True)