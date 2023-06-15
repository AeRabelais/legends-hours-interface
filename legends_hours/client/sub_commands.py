
from legends_hours.store.sqlite_db import *
from legends_hours.file_management.input import *
from legends_hours.file_management.output import *

def add_time_events(conn, args):

    print("Parsing time events report for the week.")

    report_df = parse_time_file(args.ReportFilePath)
    add_report_item(conn, report_df)

    # Message about end command.
    print(f"The time events for the report file at the following path: {args.ReportFilePath} have been ingested.")

def add_notes(conn, args):
    
    print(f"Searching the database for employee: {args.EmployeeName}, on {args.WeekDay}.")

    # Get employee first and last name and date. Find their report id for the week in the connection.
    first, last = (args.EmployeeName).split(' ')
    report_id = get_report_by_name_week(conn=conn, date=args.WeekDay, first_name=first, last_name=last)

    # If no report id is found, determine whether the employee or week-date can't be found.
    if len(report_id) < 1:
            raise ValueError(f"No entries that include the following date {args.WeekDay} could be found for employee {args.EmployeeName}. \
                             Please ensure the date is not beyond a week into the future, and that the employee was working during this time.")
 
    comment = create_comment_item(report_id, args.Comment)
    add_comment_item(conn, comment)

    # Add comment to the database.

def compile_week_hours(conn, args):
    
    print(f"Compiling total hours for the following week: {args.WeekDay}.")

    # Use get_weekly_report to get all information for the week.
    weekly_report_df = get_weekly_report(conn, args.WeekDay)

    if len(weekly_report_df.index) < 1:
        raise Warning(f"No time event report has been found for the date: {args.WeekDay}.")

    # Feed the dataframe into the output function to create the excel file.
    create_excel_with_flags(weekly_report_df, args.OutputFilePath)

def export_overtime_pdf(conn, args):

    print(f"Creating an overtime review document for the week of the following date: {args.WeekDay}.")

    overtime_comments_df = get_flagged_comments_for_week(conn, args.WeekDay)

    if len(overtime_comments_df.index) < 1:
        raise Warning("No comments regarding employee overtime have been left.")
    
    # Give information about the flagged employee, hours, and comments to compile into the PDF.
    create_pdf_with_comments(overtime_comments_df, args.OutputFilePath)

  
