
def report_table_query():

    report_table_query = """
                        CREATE TABLE IF NOT EXISTS report(
                            id INTEGER PRIMARY KEY, 
                            firstName TEXT,
                            lastName TEXT, 
                            employee TEXT,
                            hours INTEGER, 
                            startDate TEXT,
                            endDate TEXT
                            ); 
                        """

    return report_table_query

def comments_table_query():

    comments_table_query = """
                            CREATE TABLE IF NOT EXISTS comment (
                                id INTEGER PRIMARY KEY,
                                comment TEXT,
                                report_id INTEGER,
                                FOREIGN KEY (report_id) REFERENCES report (id)
                            );
                            """




