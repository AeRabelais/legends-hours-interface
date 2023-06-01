
def employee_table_query():

    employee_table_query = """CREATE TABLE IF NOT EXISTS employee(
                                id INTEGER PRIMARY KEY, 
                                employeeLegendsId TEXT, 
                                employeeFirst TEXT,
                                employeeLast TEXT,
                                UNIQUE(employeeName, employeeLegendsId)
                                ); """
    
    return employee_table_query

def hours_table_query():

    hours_table_query = """CREATE TABLE IF NOT EXISTS hours(
                            id INTEGER PRIMARY KEY, 
                            FOREIGN KEY(employee_id) REFERENCES employee (id), 
                            hours REAL, 
                            comments TEXT, 
                            start_week TEXT,
                            end_week TEXT
                            ); """

    return hours_table_query



