DEFAULT_DB_PATH = "legends_hours.db"

# MENU ITEMS
about_dialog = {
            'type': 'AboutDialog',
            'menuTitle': 'About the Interface',
            'name': 'Legends Hours Interface',
            'description': 'Replace with description of this application.',
            'version': '0.1.0',
            'copyright': '2023',
            'developer': 'Ashia Livaudais',
            'license': 'GNU GPL'
}

menu=[
        {
        'name': 'About',
        'items': [about_dialog]
        }
    ]

# EXCEL RELEVANT COLUMNS
relevant_excel_cols = ["Employee", " Reg Hours",  " Employee ID"]

## DATABASE SCHEMA

REPORT_TABLE_QUERY = """
                        CREATE TABLE IF NOT EXISTS report(
                            id TEXT PRIMARY KEY, 
                            firstName TEXT,
                            lastName TEXT, 
                            employee TEXT,
                            hours INTEGER, 
                            startDate TEXT,
                            endDate TEXT,
                            flag INTEGER
                            ); 
                        """

COMMENTS_TABLE_QUERY = """
                            CREATE TABLE IF NOT EXISTS comment (
                                id TEXT PRIMARY KEY,
                                comment TEXT,
                                report_id INTEGER,
                                FOREIGN KEY (report_id) REFERENCES report (id)
                            );
                            """

