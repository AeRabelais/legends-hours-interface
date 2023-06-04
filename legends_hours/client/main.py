from gooey.python_bindings.gooey_parser import GooeyParser 
from gooey.python_bindings.gooey_decorator import Gooey
from settings import menu
import sys 

@Gooey(program_name="Legends Time Events Interface",
        advanced=True,
        menu=menu
        )
def main():
    parser = GooeyParser(description="Legends SL Time Events Interface")
    # parser.add_argument('hours-file', help="path of the hours file to parse", widget='FileChooser') 
    
    subparsers = parser.add_subparsers(help="subcommand help")

    excel_parser = subparsers.add_parser("parse-time-events", help="Parses time events from a valid excel sheet.")
    excel_parser.add_argument("excel-file", help="The excel file containing the stored employee time events for the week.", widget="FileChooser")
    # Add notes to the employee overtime.
    notes_parser = subparsers.add_parser("add-notes", help="Add notes regarding employee overtime events.")
    notes_parser.add_argument("employee", help="Full name of the employee you'd like to comment on. Please write full name as 'FirstName LastName'.", widget="TextField")
    notes_parser.add_argument("comment", type=str, help="The comment about why the employee was allowed over time.", widget="TextField")
    notes_parser.add_argument("week-date", help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser")

    # Return the hours information for a certain week. 
    compile_hours_parser = subparsers.add_parser("compile-week-hours", help="Return an excel file with time events for the specified week.")
    compile_hours_parser.add_argument("week-date", type=str, help="The start or end date of the week you're looking for. You can also use the current date for the most recent week.", widget="DateChooser")

    # Return the over time pdf file.
    overtime_pdf_parser = subparsers.add_parser("export-overtime-pdf", help="Export the pdf listing overtime events.")
    overtime_pdf_parser.add_argument("file-path", type=str, help="The path where you'd like to place the export file", widget="DirChooser")

    args = parser.parse_args()


