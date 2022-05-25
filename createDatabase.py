import sqlite3

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"./darthouseSQLite.db")
