from gooey.python_bindings.gooey_parser import GooeyParser 
from gooey.python_bindings.gooey_decorator import Gooey
from legends_hours.store.sqlite_db import *
from legends_hours.file_management.input import *
from legends_hours.settings import menu
import sys 

def subcommand_a(args):
    conn = create_connection()

    print("Parsing time events report for the week.")

    report_df = parse_time_file(args.ReportFilePath)
    # add_report_item(conn, report_df)
    # Ingest the file.
    # Message about end command.
    print(f"The time events for the report file at the following path: {args.ReportFilePath} have been ingested.")



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
    parser = GooeyParser(description="Legends SL Time Events Interface")
    
    subparsers = parser.add_subparsers(help="subcommand help")
    
    excel_parser = subparsers.add_parser("parse-time-events", help="Parses time events from a valid csv file.", )
    excel_parser.add_argument("ReportFilePath", help="The report file containing the stored employee time events for the week.", widget="FileChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636',         'validator': {
            'test': 'not re.findall(r\"\\s\", user_input) or re.findall(r"^\\\'[^\\"\\\']+\\\'$", user_input) or re.findall(r"^\\\"[^\\\"\\\']+\\\"$", user_input)',
            'message': 'Input contains spaces and must be surrounded by quotation marks'
        }
})

    # Add notes to the employee overtime.
    notes_parser = subparsers.add_parser("add-notes", help="Add notes regarding employee overtime events.")
    notes_parser.add_argument("employeeFirstName", help="First name of the employee you'd like to comment on.", widget="FilterableDropdown",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})
    notes_parser.add_argument("employeeLastName", help="Last name of the employee you'd like to comment on.", widget="FilterableDropdown",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})
    notes_parser.add_argument("comment", type=str, help="The comment about why the employee was allowed over time.", widget="TextField",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})
    notes_parser.add_argument("week_date", help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})

    # Return the hours information for a certain week. 
    compile_hours_parser = subparsers.add_parser("compile-week-hours", help="Return an excel file with time events for the specified week.")
    compile_hours_parser.add_argument("week_date", type=str, help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})

    # Return the over time pdf file.
    overtime_pdf_parser = subparsers.add_parser("export-overtime-pdf", help="Export the pdf listing overtime events.")
    overtime_pdf_parser.add_argument("file_path", type=str, help="The path where you'd like to place the export file", widget="DirChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})

    args = parser.parse_args()
    if getattr(args, "__command", None) == "parse-time-events":
        subcommand_a(args)

# def logic(args):
    
#     print("Welcome the Legends Senior Living Hours Interface!")
#     conn = create_connection()

#     if args.command == 'parse-time-events':
#         print("Parsing time events report for the week.")

#         report_df = parse_time_file(args.ReportFilePath)
#         add_report_item(conn, report_df)
#         # Ingest the file.
#         # Message about end command.
#         print(f"The time events for the report file at the following path: {args.report_file_path} have been ingested.")
#     elif args.command == 'add-notes':
        
#         # First we need to find that report_id, and return an error if that combination can't be found.
#         # TODO: Implement report not found error.
#         report_id = get_report_by_name_week(conn=conn, date=args.week_date, 
#                                             first_name=args.employeeFirstName, 
#                                             last_name= args.employeeLastName, 
#                                             )
#         # Create the comment dataframe.
#         comment_df = create_comment_item(report_id = report_id, comment=args.comment)

#         # Add comment to the database.
#         add_comment_item(conn=conn, items_df=comment_df)
#     elif args.command == 'compile-week-hours':
#         pass


if __name__ == "__main__":
    sys.exit(main())

        
    


