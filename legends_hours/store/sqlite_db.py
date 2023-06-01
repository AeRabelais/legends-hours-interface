import sqlite3
from sqlite3 import Connection
from typing import List
from legends_hours.settings import DEFAULT_DB_PATH
from legends_hours.store.schema import hours_table_query, employee_table_query
import pandas as pd 

def create_connection(db_file: str=DEFAULT_DB_PATH) -> Connection:
    """ 
    Create a database connection to the SQLite database specified by db_file path.

    Args:
        db_file: The path to the sqlite database object being used.

    Returns:
        A sqlite3 Connection object.
    """
    conn = sqlite3.connect(db_file)

    # Add employee and hours_worked tables, if it doesn't exist.
    create_tables([employee_table_query, hours_table_query])

    return conn

def create_tables(conn: Connection, list_create_tables_sql: List[str]):
    """ 
    Creates tables that are apart of the legends hours database schema.

    Args:
        conn: a sqlite3 Connection object.
        list_create_tables_sql: A list of the queries needed to create the tables.
    """

    cursor = conn.cursor()
    for table_sql in list_create_tables_sql:
        cursor.execute(table_sql)


# Add item to the "employee" table. 
def add_employee(conn, item_df: pd.DataFrame):
    """
    Adds an employee item that holds information about each employee, namely their names and Legends ids.

    Args:
        conn: a sqlite3 Connection object.
        item_df: a dataframe with information parsed from the initial excel file.
    """

    cursor = conn.cursor()

    if len(item_df.index) > 1:
        row_lists = [tuple(item_df.loc[idx, :].values.flatten().tolist()) for idx in len(item_df.index)]
    
        cursor.executemany("""INSERT INTO employee VALUES(?, ?, ?)""", row_lists)
    else:
        cursor.execute(f"""
        INSERT OR IGNORE INTO employee VALUES
            ('{item_df['id']}', '{item_df['employeeLegendsId']}', '{item_df['employeeName']}'),
        """)
    conn.commit()

# Add item to the "hours_worked" table.
def add_hours_worked(conn, item_df: pd.DataFrame):
    """
    Adds an hours item that holds information about the hours worked by employees for each week.

    Args:
        conn: a sqlite3 Connection object.
        item_df: a dataframe with information parsed from the initial excel file.
    """

    cursor = conn.cursor()

    row_lists = [tuple(item_df.loc[idx, :].values.flatten().tolist()) for idx in len(item_df.index)]
    
    cursor.executemany("""INSERT INTO hours VALUES(?, ?, ?, ?, ?, ?)""", row_lists)
    conn.commit()

def find_employee_by_name(conn: sqlite3.Connection, employee_name: str):
    """
    Returns the employee identifier using the name.

    Args:
        conn: a sqlite3 Connection object.
        employee_name: The name of the employee of interest.

    Returns:
        The identifier used to represent the employee of interest.
    """

    cursor = conn.cursor()

    result = cursor.execute(f"""SELECT id FROM employee WHERE employeeName='{employee_name}'""")
    id = result.fetchone()

    return id
