from gooey.python_bindings.gooey_parser import GooeyParser 
from gooey.python_bindings.gooey_decorator import Gooey
from legends_hours.store.sqlite_db import *
from legends_hours.file_management.input import *
from legends_hours.settings import menu
import sys 

def parse_time_events(conn, args):

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
            raise ValueError(f"No entries that include the following date {args.WeekDay} could be found for employee {args.EmployeeName}. Please ensure the date is not beyond a week into the future, and that the employee was working during this time.")
 
    comment = create_comment_item(report_id, args.Comment)
    add_comment_item(conn, comment)

    # Add comment to the database.

def compile_week_hours(conn, args):
    
    print(f"Compiling total hours for the following week: {args.WeekDay}.")

    # Use get_weekly_report to get all information for the week.
    weekly_report_df = get_weekly_report(conn, args.WeekDay)

    # Feed the dataframe into the output function to create the excel file.


def export_overtime_pdf(conn, args):

    print(f"Creating an overtime review document for the week of the following date: {args.WeekDay}.")

    employees = get_flagged_employees(conn, args.WeekDay)

    # From each tuple, pull the id.
    employee_ids = [employee[0] for employee in employees]

    comments = []
    # Find the comments associated with these ids.
    comments = [
                {
                    "comment": get_comment_by_id(conn, employee[0]), 
                    "employee": "replace/with/name/idx", 
                    "hours": "replace/with/hours/idx",
                } 
                for employee in employees
                ] 

    if len(comments) < 1:
        raise Warning("No comments regarding employee overtime have been left.")
    
    # Give information about the flagged employee, hours, and comments to compile into the PDF.
  


@Gooey(program_name="Legends Time Events Interface",
        advanced=True,
        menu=menu,
        sidebar_title="Commands",
        header_bg_color='#363636',
        footer_bg_color="#363636",
        sidebar_bg_color="#363636",
        terminal_font_color="#ff0000",
        body_bg_color='#262626')
def main():
    conn = create_connection()
    parser = GooeyParser(description="Legends SL Time Events Interface")
    
    subparsers = parser.add_subparsers(help="subcommand help")
    
    excel_parser = subparsers.add_parser("parse-time-events", help="Parses time events from a valid csv file.", )
    excel_parser.add_argument("ReportFilePath", help="The report file containing the stored employee time events for the week.", widget="FileChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636',})

    # Add notes to the employee overtime.
    notes_parser = subparsers.add_parser("add-notes", help="Add notes regarding employee overtime events.")
    notes_parser.add_argument("EmployeeName", help="The First and Last name of the employee you'd like to comment on.", choices = find_all_employees(conn), widget="FilterableDropdown",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})
    notes_parser.add_argument("Comment", type=str, help="The comment about why the employee was allowed over time.", widget="TextField",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})
    notes_parser.add_argument("WeekDay", help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})

    # Return the hours information for a certain week. 
    compile_hours_parser = subparsers.add_parser("compile-week-hours", help="Return an excel file with time events for the specified week.")
    compile_hours_parser.add_argument("WeekDay", type=str, help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})

    # Return the over time pdf file.
    overtime_pdf_parser = subparsers.add_parser("export-overtime-pdf", help="Export the pdf listing overtime events.")
    overtime_pdf_parser.add_argument("FilePath", type=str, help="The path where you'd like to place the export file", widget="DirChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})

    args = parser.parse_args()
    if getattr(args, "__command", None) == "parse-time-events":
        parse_time_events(conn, args)
    elif getattr(args, "__command", None) == "add-notes":
        add_notes(conn, args)
    elif getattr(args, "__command", None) == "compile-week-hours":
        compile_week_hours(conn, args)
    elif getattr(args, "__command", None) == "export-overtime-pdf":
        export_overtime_pdf(conn, args)


if __name__ == "__main__":
    sys.exit(main())

        
    


