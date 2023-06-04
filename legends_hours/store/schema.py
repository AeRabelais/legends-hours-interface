
def report_table_query():

    hours_table_query = """CREATE TABLE IF NOT EXISTS report(
                            id INTEGER PRIMARY KEY, 
                            employeeFirst TEXT,
                            employeeLast TEXT, 
                            hours REAL, 
                            comments TEXT, 
                            start_week TEXT,
                            end_week TEXT
                            ); """

    return hours_table_query



