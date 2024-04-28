# sql.py
import mysql.connector
from mysql.connector import Error

def create_connection(hostname, username, userpw, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=userpw,
            database=dbname
        )
        print("CONNECTION SUCCESS")
    except Error as e:
        print(f'The error {e} occurred')
    return connection

def execute_query(connection, query, values=None, disable_foreign_keys=False):
    cursor = connection.cursor(dictionary=True)

    try:
        # Disable foreign key checks if specified
        if disable_foreign_keys:
            cursor.execute("SET foreign_key_checks = 0")

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        # Fetch results only if there are any
        rows = cursor.fetchall() if cursor.with_rows else None

    finally:
        # Re-enable foreign key checks after executing the query
        if disable_foreign_keys:
            cursor.execute("SET foreign_key_checks = 1")

        # Close the cursor
        cursor.close()

    return rows

def execute_insert(connection, query, values):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

def execute_update(connection, query, values):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

def execute_delete(connection, query, values):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

# Example usage:
if __name__ == "__main__":
    # Connection details
    conn_details = {
        'hostname': 'cis3368spring.cp0286s66hl9.us-east-2.rds.amazonaws.com',
        'username': 'admin',
        'userpw': 'Cis33682024',
        'dbname': 'Cis3368springdb'
    }

    # Connection
    conn = create_connection(**conn_details)

