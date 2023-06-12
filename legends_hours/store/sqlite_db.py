import sqlite3
from sqlite3 import Connection
from typing import List, Optional
from legends_hours.settings import DEFAULT_DB_PATH
from legends_hours.store.schema import report_table_query, comments_table_query
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
    create_tables([report_table_query, comments_table_query])

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

    item_df.to_sql('report', conn, if_exists='append', index=False)
    
# Upsert notes for a particular employee on a certain week.
def add_comment_item(conn: sqlite3.Connection, item_df: pd.DataFrame):
    
    item_df.to_sql('comment', conn, if_exists='append', index=False)


# Return report information for all employees on a given week.
def get_weekly_report(conn: sqlite3.Connection, date):

    cursor = conn.cursor()

    # Find the week containing the given date
    result = cursor.execute('''
        SELECT * FROM report
        WHERE ? BETWEEN startDate AND endDate
        ORDER BY employee
        ''', (date,))

    report = result.fetchall()  # Retrieve the first matching report item

    cursor.close()
    conn.close()

    return report

def get_report_by_name_week(conn: sqlite3.Connection, date, first_name, last_name):
    
    cursor = conn.cursor()

    # Find the report item matching the date and employee name.
    result = cursor.execute(f'''
        SELECT * FROM report
        WHERE ? BETWEEN startDate AND endDate 
        AND WHERE firstName='{first_name}' AND
        AND WHERE lastName='{last_name}'
        ORDER BY employee
        ''', (date,))

    report = result.fetchall()  # Retrieve the first matching report item

    cursor.close()
    conn.close()

    return report


# Return the report information for all flagged employees in a particular week.
def get_flagged_employees(conn: sqlite3.Connection, date):

    cursor = conn.cursor()

    # Find the week containing the given date
    result = cursor.execute('''
        SELECT * FROM report
        WHERE ? BETWEEN startDate AND endDate
        AND WHERE flag != 0
        ORDER BY employee
        ''', (date,))

    flagged_employees = result.fetchall()  # Retrieve the first matching report item

    cursor.close()
    conn.close()

    return flagged_employees


def find_employee_by_name(conn: sqlite3.Connection, first_name: Optional[str], last_name: Optional[str], employee_full_name: Optional[str]):
    """
    Returns the information related to an employee using the name.

    Args:
        conn: a sqlite3 Connection object.
        employee_name: The name of the employee of interest.

    Returns:
        The identifier used to represent the employee of interest.
    """
    if (first_name and last_name and employee_full_name ) is None:
        raise ValueError("A first, last, or full name in the format 'LastName,FirstName' must be provided.")
    
    cursor = conn.cursor()

    result = cursor.execute(f"""
                            SELECT * FROM report 
                            WHERE firstName='{first_name}' AND
                            WHERE lastName='{last_name}'
                            GROUP BY week
                            """)
    employee = result.fetchone()

    return employee

def get_comment_by_id(conn: sqlite3.Connection, report_id: str):
    
    cursor = conn.cursor()

    result = cursor.execute(f"""
                            SELECT * FROM comment
                            WHERE report_id = '{report_id}' 
                            """)
    comment = result.fetchone()

    return comment


