import pandas as pd 
from settings import relevant_excel_cols
import re
from datetime import datetime, timedelta

# Return the structured hours dataframe. 
def parse_time_file(hours_file_path: str):

    __check_file_format__(hours_file_path)

    # Return filtered down dataframe.
    time_df = ingest_time_file(hours_file_path)

    # Aggregate and group by the dataframe columns.
    parsed_time_df = time_df.groupby(['Employee', 'EmployeeID']).agg({'Reg Hours': 'sum'}).reset_index()

    # Add start date and end date columns.
    start_date, end_date = extract_week_from_title(hours_file_path)

    parsed_time_df["Start Date"] = start_date
    parsed_time_df["End Date"] = end_date
    
    return parsed_time_df 

# Read in the time report file.
def ingest_time_file(hours_file_path: str):

    time_df = pd.read_csv(hours_file_path)

    __check_columns_exist__(time_df)
    # Extract only the relevant columns.
    filtered_time_df = time_df[relevant_excel_cols]
    filtered_time_df["Reg Hours"] = filtered_time_df["Reg Hours"].astype(int)

    return filtered_time_df 

# Extract the week start and end from the time report file.
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

def __check_file_format__(hours_file_path: str):

    if not hours_file_path.endswith('.csv'):
        raise ValueError(f"The file report path: {hours_file_path} has an invalid extension.")

def __check_columns_exist__(hours_report_df: pd.DataFrame):

    for column in relevant_excel_cols:
        if column not in hours_report_df.columns:
            raise KeyError(f"The key {column} is missing from the report columns.")