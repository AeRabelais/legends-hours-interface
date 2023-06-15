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
    
    item_df.to_sql('comment', conn, if_exists='append', index=False)


# Return report information for all employees on a given week.
def get_weekly_report(conn: sqlite3.Connection, date):

    report_query = f'''
            SELECT * FROM report
            WHERE {date} BETWEEN startDate AND endDate
            ORDER BY employee
            '''
    weekly_report = pd.read_sql(report_query, conn)

    return weekly_report

def get_report_by_name_week(conn: sqlite3.Connection, date: str, first_name: str, last_name: str):
    
    cursor = conn.cursor()

    # Find the report item matching the date and employee name.
    result = cursor.execute(f'''
        SELECT * FROM report
        WHERE {date} BETWEEN startDate AND endDate 
        AND firstName='{first_name.upper()}'
        AND lastName='{last_name.upper()}'
        ORDER BY employee
        ''')

    report = result.fetchone()  # Retrieve the first matching report item

    cursor.close()

    return report


# Return the report information for all flagged employees in a particular week.
def get_flagged_employees(conn: sqlite3.Connection, date: str):

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

def get_flagged_comments_for_week(conn: sqlite3.Connection, date: str):

    flagged_comments_query = """
                            SELECT r.employee, r.hours, r.flag, c.comment
                            FROM report r
                            INNER JOIN comment c ON r.id = c.report_id
                            WHERE {date} BETWEEN r.startDate AND r.endDate
                            """
    
    flag_comments = pd.read_sql(flagged_comments_query, conn)

    return flag_comments

# def find_employee_by_name(conn: sqlite3.Connection, first_name: Optional[str], last_name: Optional[str], employee_full_name: Optional[str]):
#     """
#     Returns the information related to an employee using the name.

#     Args:
#         conn: a sqlite3 Connection object.
#         employee_name: The name of the employee of interest.

#     Returns:
#         The identifier used to represent the employee of interest.
#     """
#     if (first_name and last_name and employee_full_name ) is None:
#         raise ValueError("A first, last, or full name in the format 'LastName,FirstName' must be provided.")
    
#     cursor = conn.cursor()

#     result = cursor.execute(f"""
#                             SELECT id FROM report 
#                             WHERE firstName='{first_name}' AND
#                             lastName='{last_name}'
#                             GROUP BY startDate
#                             """)
#     employee = result.fetchone()

#     return employee

def find_all_employee_names(conn: sqlite3.Connection):

    employees_query = "SELECT DISTINCT firstName || ' ' || lastName AS fullName FROM reports"

    all_employees = pd.read_sql(employees_query, conn)

    return all_employees['fullName']


# def get_comment_by_id(conn: sqlite3.Connection, report_id: str):
    
#     cursor = conn.cursor()

#     result = cursor.execute(f"""
#                             SELECT * FROM comment
#                             WHERE report_id = '{report_id}' 
#                             """)
#     comment = result.fetchone()

#     return comment

