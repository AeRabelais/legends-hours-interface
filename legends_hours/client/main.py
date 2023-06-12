from gooey.python_bindings.gooey_parser import GooeyParser 
from gooey.python_bindings.gooey_decorator import Gooey
from legends_hours.store.sqlite_db import *
from legends_hours.file_management.input import *
from settings import menu
import sys 

@Gooey(program_name="Legends Time Events Interface",
        advanced=True,
        menu=menu
        )
def parse_args():
    parser = GooeyParser(description="Legends SL Time Events Interface")
    
    subparsers = parser.add_subparsers(help="subcommand help")

    excel_parser = subparsers.add_parser("parse-time-events", help="Parses time events from a valid csv file.")
    excel_parser.add_argument("report_file_path", help="The report file containing the stored employee time events for the week.", widget="FileChooser")

    # Add notes to the employee overtime.
    notes_parser = subparsers.add_parser("add-notes", help="Add notes regarding employee overtime events.")
    notes_parser.add_argument("employeeFirstName", help="First name of the employee you'd like to comment on.", widget="FilterableDropdown")
    notes_parser.add_argument("employeeLastName", help="Last name of the employee you'd like to comment on.", widget="FilterableDropdown")
    notes_parser.add_argument("comment", type=str, help="The comment about why the employee was allowed over time.", widget="TextField")
    notes_parser.add_argument("week_date", help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser")

    # Return the hours information for a certain week. 
    compile_hours_parser = subparsers.add_parser("compile-week-hours", help="Return an excel file with time events for the specified week.")
    compile_hours_parser.add_argument("week_date", type=str, help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser")

    # Return the over time pdf file.
    overtime_pdf_parser = subparsers.add_parser("export-overtime-pdf", help="Export the pdf listing overtime events.")
    overtime_pdf_parser.add_argument("file_path", type=str, help="The path where you'd like to place the export file", widget="DirChooser")

    args = parser.parse_args()
    return args

def logic(args):
    
    print("Welcome the Legends Senior Living Hours Interface!")
    conn = create_connection()

    if args.command == 'parse-time-events':
        print("Parsing time events report for the week.")

        report_df = parse_time_file(args.report_file_path)
        add_report_item(conn, report_df)
        # Ingest the file.
        # Message about end command.
        print(f"The time events for the report file at the following path: {args.report_file_path} have been ingested.")
    elif args.command == 'add-notes':
        
        # First we need to find that report_id, and return an error if that combination can't be found.
        # TODO: Implement report not found error.
        report_id = get_report_by_name_week(conn=conn, date=args.week_date, 
                                            first_name=args.employeeFirstName, 
                                            last_name= args.employeeLastName, 
                                            )
        # Create the comment dataframe.
        comment_df = create_comment_item(report_id = report_id, comment=args.comment)

        # Add comment to the database.
        add_comment_item(conn=conn, items_df=comment_df)
    elif args.command == 'compile-week-hours':
        pass

def main():
    
    args = parse_args()
    logic(parse_args())



        
    


