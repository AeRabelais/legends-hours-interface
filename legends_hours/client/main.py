from gooey.python_bindings.gooey_parser import GooeyParser 
from gooey.python_bindings.gooey_decorator import Gooey
from settings import menu
import sys 

@Gooey(program_name="Legends Hours Interface",
        advanced=True,
        menu=menu
        )
def main():
    parser = GooeyParser(description="Legends Senior Living Hours Interface")
    # parser.add_argument('hours-file', help="path of the hours file to parse", widget='FileChooser') 
    
    subparsers = parser.add_subparsers(help="subcommand help")

    excel_parser = subparsers.add_parser("parse-hours", help="Takes an excel sheet with employee hours and extracts overtime data.")
    excel_parser.add_argument("excel-file", help="The excel file containing the stored employee hours for the week.", widget="FileChooser")
    # Add notes to the employee overtime.
    notes_parser = subparsers.add_parser("add-notes", help="Add notes about an employee explaining over-time.")
    notes_parser.add_argument("employee", help="First, last, or first and last name of the employee that you want to leave a comment on.", widget="TextField")
    notes_parser.add_argument("comment", type=str, help="The comment about why the employee was allowed over time.", widget="TextField")
    notes_parser.add_argument("week-day", help="The start or end date of the week you're looking for. Or 'current' for the most recent week.", widget="DateChooser")

    # Return the hours information for a certain week. 
    compile_hours_parser = subparsers.add_parser("compile-week-hours", help="Return a remade excel sheet for a particular week.")
    compile_hours_parser.add_argument("week-day", type=str, help="The start or end date of the week you're looking for. Or 'current' for the most recent week.", widget="DateChooser")

    # Return the over time pdf file.
    overtime_pdf_parser = subparsers.add_parser("export-overtime-pdf", help="Export the pdf listing overtime information.")
    overtime_pdf_parser.add_argument("file-path", type=str, help="The path where you'd like to place the export file", widget="FileChooser")

    args = parser.parse_args()


