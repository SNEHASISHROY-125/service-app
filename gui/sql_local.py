import sqlite3 , os

'''
SQL for local database | app
'''

global user_table_sql
global settings_table_sql

# 1
def check_db_exists(db_file):
    """ check if the database exists / create it if not """
    try:
        if not os.path.exists(db_file): # if not exists
            conn = create_connection(db_file)
            # initialize the database
            initialize_db(conn)
            # insert default settings
            insert_data(conn, 'settings', {'app_first_run': 1, 'app_theme': 'Light'})
            # insert default user
            insert_data(conn, 'users', {'user_id': 'xyz', 'password': 'xyz', 'name': 'xyz', 'email': 'xyz'})
            return conn
        else:
            return create_connection(db_file)
    except Exception as e:
        print(e)
        return 'error'

# 3
def initialize_db(conn):
    """ initialize the database with required tables """
    global user_table_sql
    global settings_table_sql
    user_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """
    settings_table_sql = """
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_first_run BOOLEAN NOT NULL,
        app_theme TEXT NOT NULL
    );
    """
    create_table(conn, user_table_sql)
    create_table(conn, settings_table_sql)
    
# 2
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        return 'error'

# 4
def insert_data(conn, table, data: dict):
    """
    Insert data into a specified table in the database.

    Args:
        conn (sqlite3.Connection): The connection object to the SQLite database.
        table (str): The name of the table where data will be inserted.
        data (dict): A dictionary containing the column names as keys and the corresponding values to be inserted.

    Returns:
        str: Returns 'error' if an SQLite error occurs, otherwise returns None.
    """
    """ insert data into table """
    keys = ', '.join(data.keys())
    question_marks = ', '.join(list('?'*len(data)))
    values = tuple(data.values())
    sql = f'INSERT INTO {table} ({keys}) VALUES ({question_marks})'
    try:
        c = conn.cursor()
        c.execute(sql, values)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        return 'error'

# 6
def update_data(conn, table, data: dict, condition: dict):
    """
    Update data in a specified table in the database.

    Args:
        conn (sqlite3.Connection): The connection object to the SQLite database.
        table (str): The name of the table where data will be updated.
        data (dict): A dictionary containing the column names as keys and the corresponding values to be updated.
        condition (dict): A dictionary containing the column names as keys and the corresponding values to be used in the WHERE clause.

    Returns:
        str: Returns 'error' if an SQLite error occurs, otherwise returns None.
    """
    """ update data in table """
    keys = ', '.join(data.keys())
    values = tuple(data.values())
    set_values = ', '.join([f'{key} = ?' for key in data.keys()])
    condition_keys = list(condition.keys())
    condition_values = tuple(condition.values())
    where_clause = ' AND '.join([f'{key} = ?' for key in condition.keys()])
    sql = f'UPDATE {table} SET {set_values} WHERE {where_clause}'
    try:
        c = conn.cursor()
        c.execute(sql, values + condition_values)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        return 'error'

# 5
def query_data(conn, query):
    """
    Query data from the database.

    Parameters:
    conn (sqlite3.Connection): The database connection object.
    query (str): The SQL query to be executed.

    Returns:
    list: A list of tuples containing the query results if successful.
    str: 'error' if an exception occurs during the query execution.
    """
    """ query data from the database """
    try:
        c = conn.cursor()
        c.execute(query)
        return c.fetchall()
    except sqlite3.Error as e:
        print(e)
        return 'error'