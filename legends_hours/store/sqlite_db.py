import sqlite3
from sqlite3 import Connection
from typing import List, Optional
from legends_hours.settings import DEFAULT_DB_PATH, REPORT_TABLE_QUERY, COMMENTS_TABLE_QUERY
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
    create_tables(conn, [REPORT_TABLE_QUERY, COMMENTS_TABLE_QUERY])

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
    """
    Adds a comment item that holds information regarding the context of employee overtime.

    Args:
        conn: a sqlite3 Connection object.
        item_df: a dataframe with information parsed from the initial excel file.
    """
    item_df.to_sql('comment', conn, if_exists='append', index=False)


# Return report information for all employees on a given week.
def get_weekly_report(conn: sqlite3.Connection, date: str) -> pd.DataFrame:
    """
    Returns the hours report associated with a given date.

    Args:
        conn: a sqlite3 Connection object.
        date: A date in the range of the start and end date associated with the desired report.
    
    Returns:
        A dataframe with the hours report for the specified date.
    """
    report_query = f'''
            SELECT * FROM report
            WHERE '{date}' BETWEEN startDate AND endDate
            ORDER BY employee
            '''
    
    weekly_report = pd.read_sql(report_query, conn)

    return weekly_report

def get_report_by_name_week(conn: sqlite3.Connection, date: str, first_name: str, last_name: str):
    """
    Returns the report identifier for the specified employee during some specified week.

    Args:
        conn: A sqlite3 Connection object.
        date: The desired date of the weekly report.
        first_name: The employee's first name.
        last_name: The employee's last name.
    
    Returns:
        The report identifier for the report item representing a specific week and employee.
    """
    cursor = conn.cursor()

    # Find the report item matching the date and employee name.
    result = cursor.execute(f'''
        SELECT * FROM report
        WHERE '{date}' BETWEEN startDate AND endDate 
        AND firstName='{first_name.upper()}'
        AND lastName='{last_name.upper()}'
        ORDER BY employee
        ''')

    report = result.fetchone()  # Retrieve the first matching report item

    cursor.close()

    return report


# Return the report information for all flagged employees in a particular week.
def get_flagged_employees(conn: sqlite3.Connection, date: str) -> list:
    """
    Fetches the employees who have been flagged, or whom have a flag value other than zero.

    Args:
        conn: A sqlite3 Connection object.
        date: The date containing the desired information.

    Returns:
        A list of the report items associated with flagged employees in a given week.
    """
    cursor = conn.cursor()

    # Find the week containing the given date
    result = cursor.execute(f'''
        SELECT * FROM report
        WHERE '{date}' BETWEEN startDate AND endDate
        AND flag != 0
        ORDER BY employee
        ''')

    flagged_employees = result.fetchall()  # Retrieve the first matching report item

    cursor.close()

    return flagged_employees

def get_flagged_comments_for_week(conn: sqlite3.Connection, date: str) -> pd.DataFrame:
    """
    Returns the flagged employees and comments for a particular week.

    Args:
        conn: A sqlite3 Connection object.
        date: The date containing the desired information.

    Returns:
        A dataframe of the report items associated with flagged employees in a given week.

    """
    flagged_comments_query = f"""
                            SELECT r.employee, r.hours, r.flag, c.comment, r.startDate
                            FROM report r
                            LEFT JOIN comment c ON r.id = c.report_id
                            WHERE '{date}' BETWEEN r.startDate AND r.endDate
                            AND (r.hours > 35 OR c.comment IS NOT NULL)
                            ORDER BY c.comment IS NULL, r.hours DESC, r.employee
                            """
    
    flag_comments = pd.read_sql(flagged_comments_query, conn)

    return flag_comments

def find_all_employee_names(conn: sqlite3.Connection) -> list:
    """
    Returns all of the unique employee names in the database in 'firstName lastName' pairs.

    conn: a sqlite3 Connection object.

    Returns:
        A list of the all the employee names.
    """

    employees_query = "SELECT DISTINCT firstName || ' ' || lastName AS fullName FROM report"

    all_employees = pd.read_sql(employees_query, conn)

    return list(all_employees['fullName'])
