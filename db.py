import sqlite3

def create_database(schema_filename, db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    with open(schema_filename) as schema_file:
        schema = schema_file.read()

    cursor.execute(schema)

    conn.commit()

    return conn
