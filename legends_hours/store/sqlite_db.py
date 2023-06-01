import sqlite3
# Create or connect to the database.


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



# Create the database schema if the database path does not exist.

# Add item to the "employee" table. 

# Add item to the "hours_worked" table.

# Upsert hours to the "hours_worked" table.

# Upsert comments to the "hours_worked" table.