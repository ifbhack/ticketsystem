import sqlite3

schema_filename = "schema.sql"

def create_database(db_filename: str):
    conn = sqlite3.connect(db_filename)

    with open(schema_filename) as schema_file:
        conn.executescript(schema_file.read())

    return conn
