import uuid
import numpy as np
import pandas as pd 
from legends_hours.settings import relevant_excel_cols
import re
from datetime import datetime, timedelta

def create_comment_item(report_id: str, comment: str):

    comment_dict = {"id": [str(uuid.uuid4())], "comment": [comment], "report_id": [report_id]}
    comment = pd.DataFrame(comment_dict)

    return comment 

# Return the structured hours dataframe. 
def parse_time_file(hours_file_path: str):

    __check_file_format__(hours_file_path)

    # Return filtered down dataframe.
    time_df = ingest_time_file(hours_file_path)

    # Aggregate and group by the dataframe columns.
    parsed_time_df = time_df.groupby(['Employee']).agg({' Reg Hours': 'sum'}).reset_index()

    # Make first name and last name columns that are a split of the employee name on the comma.
    parsed_time_df['firstName'] = parsed_time_df['Employee'].str.split(',').str[1].str.upper().str.strip()
    parsed_time_df['lastName'] = parsed_time_df['Employee'].str.split(',').str[0].str.upper().str.strip()

    # Add an id column that produces a unique UUID for each employee.
    parsed_time_df['id'] = parsed_time_df.apply(lambda row: str(uuid.uuid4()), axis=1)

    # Add flag column. Add values 0, to employees within the right time, 1 to employees ~36, 2 to employess ~40
    conditions = [
        parsed_time_df[' Reg Hours'] < 35,
        (parsed_time_df[' Reg Hours'] >= 35) & (parsed_time_df[' Reg Hours'] < 40),
        parsed_time_df[' Reg Hours'] >= 40
    ]
    choices = [0, 1, 2]

    parsed_time_df['flag'] = np.select(conditions, choices, default=0)

    # Rename the hours and employee columns.
    parsed_time_df.rename(columns={" Reg Hours": "hours", "Employee": "employee"}, inplace=True)

    # Add start date and end date columns.
    start_date, end_date = extract_week_from_title(hours_file_path)

    parsed_time_df["startDate"] = start_date
    parsed_time_df["endDate"] = end_date
        
    return parsed_time_df 

# Read in the time report file.
def ingest_time_file(hours_file_path: str):

    time_df = pd.read_csv(hours_file_path)

    __check_columns_exist__(time_df)
    # Extract only the relevant columns.
    filtered_time_df = time_df[relevant_excel_cols]
    filtered_time_df[" Reg Hours"] = filtered_time_df[" Reg Hours"].astype(int)

    return filtered_time_df 

# Extract the week start and end from the time report file.
def extract_week_from_title(hours_file_path: str):

    parsed_match = re.findall(r"\d{1,2}-\d{1,2}-\d{4}", hours_file_path)

    if parsed_match is None:
        raise ValueError("No corresponding start date could be extracted for the input file.")
    else:
        date_objects = [datetime.strptime(match, "%m-%d-%Y").date() for match in parsed_match]
        print(date_objects)

        start_date, end_date = date_objects[0], date_objects[1]
    return start_date, end_date

def __check_file_format__(hours_file_path: str):

    if not hours_file_path.endswith('.csv'):
        raise ValueError(f"The file report path: {hours_file_path} has an invalid extension.")

def __check_columns_exist__(hours_report_df: pd.DataFrame):

    for column in relevant_excel_cols:
        if column not in hours_report_df.columns:
            raise KeyError(f"The key {column} is missing from the report columns.")