"""
Parse the uploaded excel sheet. Return the employee, employeeId, regularHours, start of week, and end of week.
Extract start of the week and end of the week from the name of the report file.

"""
import pandas as pd 
from settings import relevant_excel_cols
import re
from datetime import datetime, timedelta

# Return the structured hours dataframe. 
def parse_time_file(hours_file_path: str):

    # Return filtered down dataframe.
    time_df = ingest_time_file(hours_file_path)

    # Aggregate and group by the dataframe columns.
    parsed_time_df = time_df.groupby(['Employee', 'EmployeeID']).agg({'Reg Hours': 'sum'}).reset_index()

    # Add start date and end date columns.
    start_date, end_date = extract_week_from_title(hours_file_path)

    parsed_time_df["Start Date"] = start_date
    parsed_time_df["End Date"] = end_date
    
    return parsed_time_df 


# Read in the excel file.
def ingest_time_file(hours_file_path: str):

    time_df = pd.read_excel(hours_file_path)

    # Extract only the relevant columns.
    filtered_time_df = time_df[relevant_excel_cols]
    filtered_time_df["Reg Hours"] = filtered_time_df["Reg Hours"].astype(int)

    return filtered_time_df 

# Extract the week start and end from the excel file.
def extract_week_from_title(hours_file_path: str):

    parsed_start_match = re.search("^\d{1,2}-\d{1,2}-\d{4}$", hours_file_path)

    if parsed_start_match is None:
        raise ValueError("No corresponding start date could be extracted for the input file.")
    else:
        # Turn the parsed date into a datetime object.
        start_date = parsed_start_match.group(0)
        start_date_obj = datetime.strptime(start_date, '%m-%d-%y').date()

        # Add seven days to accounts for the end of a week.
        end_date = start_date + timedelta(days=7)

    return start_date, end_date


