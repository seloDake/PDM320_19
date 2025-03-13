"""
import psycopg2

# Replace these values with your actual database connection details
host = "127.0.0.1"         # The host of the database
port = "5432"              # The port (default: 5432)
dbname = "p32001_19"    # The database name
user = ""     # Your PostgreSQL username
password = "" # Your PostgreSQL password

# Establish a connection to the PostgreSQL database
try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Test the connection by running a query
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("PostgreSQL database version:", db_version)

    # Don't forget to close the connection
    cursor.close()
    connection.close()

except Exception as error:
    print(f"Error: {error}")"
"""

import psycopg2
from sshtunnel import SSHTunnelForwarder

username = "osj7577"
password = "histet-Jubrih-5zygda"
dbName = "p32001_19"


try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('127.0.0.1', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'database': dbName,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }


        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")

        #DB work here....

        conn.close()
except:
    print("Connection failed")
