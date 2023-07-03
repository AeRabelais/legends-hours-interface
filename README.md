# Legends Hours Interface

The Legends Hours Interface is an executable application that allows users to aggregate, analyze, and create reports based on input files tracking employee hours.

## Required Files
In order to add information from a report sheet to the interface's database, a valid report sheet, in the form of a CSV or Excel file must be provided. 

### Required File Structure

#### Must Include the Week Date
The file's name must include the week associated with its information in the following format: M-DD-YYYY-M-DD-YYYY, where the month (M) can be written using one or two digits.
For instance, a valid name would be: `5-28-2023-6-3-2023_River-Oaks_Bi-Weekly_punch-detail-report`. 

#### Must Include Certain Columns
Certain columns must be included in the report sheet. Those columns are as follows: `"Employee", " Reg Hours",  " Employee ID"`. Please ensure that your input report sheet
at least has these columns.

#### Must Have the Right Extension
The input report sheet must either be a CSV file or Excel sheet. Please ensure that your file ends with either of the relevant extensions: `.csv` or `.xlsx`.

## Instructions for Use

The application has four primary commands that users can access. Those are the following: `add-time-events`, `add-notes`, `compile-week-hours`, and `export-overtime-pdf`.
Before any of the other subcommands can be run, the user must first ensure that the database contains information from at least one report. If you don't yet have a report, 
or the report you have contains incorrect information, please use the report file in the directory of this repository at the path `tests/files` to find an example of a valid report.
Using this file, the following instructions will show users how to interact with the application.

To begin using the application, open the executable's zip file and click `legends_hours_interface.exe`. 

### Add Time Events
As mentioned above, before you can run any other subcommands, the user must first ensure some data has been input to the database. In the sidebar of the application, click
`add-time-events`. In the main menu, you will see a label `ReportFilePath`. Press the `Browse` button to open your computer's file system and navigate to the hours report 
csv or excel file you would like to add to the database.

Press `Start` to begin the ingestion process. Once your file has been successfully ingested, you will see a pop-up message saying that your file has been successfully processed. 
Click `Cancel` to exit the application.

* Note: If you are ingesting a file, you must first exit and restart the application to run other subcommands.

### Add Notes
Open the application using the .exe file. To add comments to a user's hour information for the week, click the command `add-notes` in the sidebar of the application. 
You will see three arguments: `EmployeeName`, `Comments`, and `WeekDay`. In employee name, begin typing the first or last name of the employee you'd like to leave a comment on.
Click their name in the dropdown list of employees when they show up. In comments, type the comment you'd like to leave about the employee's overtime for the week. For weekdate,
press the `Find Date` button. In the pop up, type date month, day, and year of the week you'd like to leave a comment for. Press the white button underneath the date when you've
set the appropriate values.

Next, click `Start` at the bottom of the application window to add your notes to the database.

Upon success, a pop-up will verify that your comments have been added.

If you'd like to run another sub-command, press `Edit` at the bottom of the application screen. If not, you can exit the application.

### Compile Week Hours
Open the application using the .exe file. To return the aggregated and flagged weekly hours for all employees during a particular week, click the command `compile-week-hours` 
in the sidebar of the application. You will see two arguments: `OutputFilePath` and `WeekDay`. For the output file path, press the `Browse` button to access your computer's
local directories. Choose the folder on your machine where you'd like your excel file to be placed. For the week day, choose a date that would land in the range of the start and 
end date of the week associated with your compiled report of interest. In the pop up, type date month, day, and year of the week you'd like to leave a comment for. Press the white button underneath the date when you've
set the appropriate values.

Next, click `Start` at the bottom of the application window to compile the report from the database.

Upon success, a pop-up will verify that your comments have been added.

If you'd like to run another sub-command, press `Edit` at the bottom of the application screen. If not, you can exit the application.

### Export Overtime PDF
Open the application using the .exe file. To return the pdf for the overtime employee data and comments, click the command `export-overtime-pdf` in the sidebar of the application.
You will see two arguments: `OutputFilePath` and `WeekDay`. For the output file path, press the `Browse` button to access your computer's
local directories. Choose the folder on your machine where you'd like your PDF file to be placed. For the week day, choose a date that would land in the range of the start and 
end date of the week associated with your PDF of interest. In the pop up, type date month, day, and year of the week you'd like to leave a comment for. Press the white button underneath the date when you've
set the appropriate values.

Next, click `Start` at the bottom of the application window to compile the report from the database.

Upon success, a pop-up will verify that your comments have been added.

If you'd like to run another sub-command, press `Edit` at the bottom of the application screen. If not, you can exit the application.
