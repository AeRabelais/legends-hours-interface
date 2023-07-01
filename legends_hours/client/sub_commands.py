
from legends_hours.store.sqlite_db import *
from legends_hours.file_management.input import *
from legends_hours.file_management.output import *
import os 
from sqlite3 import Connection


def add_time_events(conn: Connection , args) -> None:
    """
    Adds a time event to the database from the command line.

    Args:
        conn: A connection object for the database.
        args: The args object for interfacing with the command line.
    """
    print("Parsing time events report for the week.")

    report_df = parse_time_file(args.ReportFilePath)
    add_report_item(conn, report_df)

    # Message about end command.
    print(f"The time events for the report file have been ingested.")

def add_notes(conn: Connection, args) -> None:
    """
    Adds overtime comments to the database for a specified employee.

    Args:
        conn: A connection object for the database.
        args: The args object for interfacing with the command line.

    Raises:
        ValueError: When a report identifier for the specified combination of employee and date can not be found.

    """
    
    print(f"Searching the database for employee: {args.EmployeeName}, on {args.WeekDay}.")

    # Get employee first and last name and date. Find their report id for the week in the connection.
    first, last = (args.EmployeeName).split(' ')
    report_id = get_report_by_name_week(conn=conn, date=args.WeekDay, first_name=first, last_name=last)
    # If no report id is found, determine whether the employee or week-date can't be found.
    if len(report_id) < 1:
            raise ValueError(f"No entries that include the following date {args.WeekDay} could be found for employee {args.EmployeeName}. \
                             Please ensure the date is not beyond a week into the future, and that the employee was working during this time.")
 
    comment = create_comment_item(report_id[0], args.Comment)
    add_comment_item(conn, comment)

    # Add comment to the database.
    print("Comment added to the database!")

def compile_week_hours(conn: Connection, args) -> None:
    """
    Compiles the total hours for each employee during the week and produces an excel file.

    Args:
        conn: A connection object for the database.
        args: The args object for interfacing with the command line.

    Raises:
        Warning: if no time report could be found for the user-specified date.

    """
    print(f"Compiling total hours for the following week: {args.WeekDay}.")

    # Use get_weekly_report to get all information for the week.
    weekly_report_df = get_weekly_report(conn, args.WeekDay)

    if len(weekly_report_df.index) < 1:
        raise Warning(f"No time event report has been found for the date: {args.WeekDay}.")

    # Feed the dataframe into the output function to create the excel file.
    create_excel_with_flags(weekly_report_df, os.path.join(args.OutputFilePath, f"report_{args.WeekDay}_hours.xlsx"))

    print(f"The compiled hours excel file has been created at the following path:{args.OutputFilePath}")

def export_overtime_pdf(conn: Connection, args) -> None:
    """
    Creates a pdf with listing of employees who have worked overtime and any comments.

    Args:
        conn: A connection object for the database.
        args: The args object for interfacing with the command line.

    Raises:
        Warning: If no employee overtime nor comments could be found about employees.

    """

    print(f"Creating an overtime review document for the week of the following date: {args.WeekDay}.")

    overtime_comments_df = get_flagged_comments_for_week(conn, args.WeekDay)
    overtime_comments_df['num_overtime'] = overtime_comments_df['hours'] - 40
    overtime_comments_df.loc[overtime_comments_df['num_overtime'] < 0, 'num_overtime'] = 0

    if len(overtime_comments_df.index) < 1:
        raise Warning("No employees have been working overtime or have comments associated with their hours.")
    
    # Give information about the flagged employee, hours, and comments to compile into the PDF.
    create_pdf_with_comments(overtime_comments_df, os.path.join(args.OutputFilePath, f"overtime_review_{args.WeekDay}.pdf"))

    print(f"The overtime review report has been created at the following path:{args.OutputFilePath}")
  
