import sqlite3


def initialize_database(db_path='company.db'):
    """
    Initializes the SQLite database and creates the required tables.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        sqlite3.Connection: Connection object to the database.
    """
    connector = sqlite3.connect(db_path, check_same_thread=False)
    db_cursor = connector.cursor()

    db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        salary REAL NOT NULL
    )
    ''')
    connector.commit()
    return connector


def create_tables(cursor, connector):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        salary REAL NOT NULL
    )
    ''')
    connector.commit()