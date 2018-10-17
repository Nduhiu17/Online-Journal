import os  # import os

import psycopg2


def connect_to_db():
    '''Function to create a database connection'''
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    conn.autocommit = True
    cursor = conn.cursor()

    return cursor

    # method that creates table users
def create_users_table():
    cursor = connect_to_db()
    sql_command = """ CREATE TABLE IF NOT EXISTS  users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(225) NOT NULL,
        date_created VARCHAR(80),
        date_modified VARCHAR(80)
            )
            """
    cursor.execute(sql_command)

# method that creates entries table
def create_entries_table():
    cursor = connect_to_db()
    sql_command = """
    CREATE TABLE IF NOT EXISTS "public"."entries"  (
        id SERIAL ,
        user_id INTEGER NOT NULL,
        date_created VARCHAR(80),
        date_modified VARCHAR(80),
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
    cursor.execute(sql_command)

# method that drops users table
def drop_users_table():
    cursor = connect_to_db()
    sql_command = """
                  DROP TABLE IF EXISTS users CASCADE;
                  """
    cursor.execute(sql_command)

# method that drops entries table
def drop_entries_table():
    cursor = connect_to_db()
    sql_command = """
                  DROP TABLE IF EXISTS entries CASCADE;
                  """
    cursor.execute(sql_command)
