import sqlite3
from sqlite3 import Error

'''
modify existing database eg modifying table and insert new data
'''

def connect_and_modify_db(db_file, table_query, insert_data):
	try:
		conn = sqlite3.connect(db_file)
		cursor = conn.cursor()
		
		# Execute table modification query
		cursor.execute(table_query)
		
		# Execute insert statement
		cursor.executemany('INSERT INTO users VALUES (?,?,?)', insert_data)
		
		conn.commit()
		print("Database modified successfully")
		
	except Error as e:
		print(f"Error: {e}")
	finally:
		if conn:
			conn.close()

# Example usage:
# table_query = "ALTER TABLE users ADD COLUMN age INTEGER"
# data = [(1, 'John', 25), (2, 'Jane', 30)]
# connect_and_modify_db('mydatabase.db', table_query, data)