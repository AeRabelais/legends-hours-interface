from gooey.python_bindings.gooey_parser import GooeyParser 
from gooey.python_bindings.gooey_decorator import Gooey
from gooey.gui.util.freeze import localResourcePath
from legends_hours.store.sqlite_db import *
from legends_hours.file_management.input import *
from legends_hours.settings import menu
from legends_hours.client.sub_commands import *
from legends_hours.settings import DEFAULT_DB_PATH, DEFAULT_ICON_PATH
import sys 


@Gooey(program_name="Legends Time Report Interface",
        advanced=True,
        menu=menu,
        sidebar_title="Commands",
        header_bg_color='#363636',
        footer_bg_color="#363636",
        sidebar_bg_color="#363636",
        terminal_font_color="#ff0000",
        body_bg_color='#262626',
        image_dir= localResourcePath(DEFAULT_ICON_PATH))
def main():

    conn = create_connection(db_file=localResourcePath(DEFAULT_DB_PATH))
    parser = GooeyParser(description="Legends SL Time Report Interface")
    
    subparsers = parser.add_subparsers(help="subcommand help", dest='command')
    
    excel_parser = subparsers.add_parser("parse-time-events", help="Parses time events from a valid csv file.", )
    excel_parser.add_argument("ReportFilePath", help="The report file containing the stored employee time events for the week.", widget="FileChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636',})

    # Add notes to the employee overtime.
    notes_parser = subparsers.add_parser("add-notes", help="Add notes regarding employee overtime events.")
    notes_parser.add_argument("EmployeeName", help="The First and Last name of the employee you'd like to comment on.", choices = find_all_employee_names(conn), widget="FilterableDropdown",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})
    notes_parser.add_argument("Comment", type=str, help="The comment about why the employee was allowed over time.", widget="TextField",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})
    notes_parser.add_argument("WeekDay", help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})


    # Return the hours information for a certain week. 
    compile_hours_parser = subparsers.add_parser("compile-week-hours", help="Return an excel file with time events for the specified week.")
    compile_hours_parser.add_argument("WeekDay", type=str, help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})
    compile_hours_parser.add_argument("OutputFilePath", type=str, help="The directory where you want the file to be held.", widget="DirChooser", gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})

    # Return the over time pdf file.
    overtime_pdf_parser = subparsers.add_parser("export-overtime-pdf", help="Export the pdf listing overtime events.")
    overtime_pdf_parser.add_argument("WeekDay", type=str, help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser",gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})
    overtime_pdf_parser.add_argument("OutputFilePath", type=str, help="The directory where you want the file to be held.", widget="DirChooser", gooey_options = {'label_color': '#ffffff', 'description_color': '#363636'})

    args = parser.parse_args()

    if args.command == 'parse-time-events': 
        add_time_events(conn, args)
    elif args.command == 'add-notes': 
        add_notes(conn, args)
    elif args.command == 'compile-week-hours':
        compile_week_hours(conn, args)
    elif args.command == 'export-overtime-pdf':
        export_overtime_pdf(conn, args)
    else:
        raise ValueError("You've entered an invalid command.")


if __name__ == "__main__":
    sys.exit(main())

        
    


