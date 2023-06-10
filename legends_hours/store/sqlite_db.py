import sqlite3
from sqlite3 import Connection
from typing import List
from legends_hours.settings import DEFAULT_DB_PATH
from legends_hours.store.schema import report_table_query
import pandas as pd 
from datetime import datetime

def create_connection(db_file: str=DEFAULT_DB_PATH) -> Connection:
    """ 
    Create a database connection to the SQLite database specified by db_file path.

    Args:
        db_file: The path to the sqlite database object being used.

    Returns:
        A sqlite3 Connection object.
    """
    conn = sqlite3.connect(db_file)

    # Add report table, if it doesn't exist.
    create_tables([report_table_query])

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


# Add item to the "report" table.
def add_report_item(conn, item_df: pd.DataFrame):
    """
    Adds a report item that holds information about the hours worked by employees for each week.

    Args:
        conn: a sqlite3 Connection object.
        item_df: a dataframe with information parsed from the initial excel file.
    """

    cursor = conn.cursor()

    row_lists = [tuple(item_df.loc[idx, :].values.flatten().tolist()) for idx in len(item_df.index)]
    
    cursor.executemany("""INSERT INTO report VALUES(?, ?, ?, ?, ?, ?, ?)""", row_lists)
    conn.commit()

# Upsert notes for a particular employee on a certain week.
def add_time_notes(conn: sqlite3.Connection, notes: str):
    pass

# Return report information for all employees on a given week.
def get_weekly_report(conn: sqlite3.Connection, week):
    pass

# Return the report information for all flagged employees in a particular week.
def get_flagged_employees(conn: sqlite3.Connection, week):
    pass



# TODO: Rewrite this to account for new tables.
def find_employee_by_name(conn: sqlite3.Connection, employee_name: str):
    """
    Returns the information related to an employee using the name.

    Args:
        conn: a sqlite3 Connection object.
        employee_name: The name of the employee of interest.

    Returns:
        The identifier used to represent the employee of interest.
    """

    cursor = conn.cursor()

    result = cursor.execute(f"""SELECT * FROM report WHERE employeeName='{employee_name}'""")
    employee = result.fetchone()

    return employee

def __check_week_exists__():
    """
    Checks whether a report for the week on the input file has already been entered.
    """
