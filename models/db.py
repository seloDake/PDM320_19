import psycopg2
from sshtunnel import SSHTunnelForwarder

# Database credentials
username = "knn4602"
password = "Kainakaren1$"
dbName = "p32001_19"

conn = None
server = None

# Function to establish the DB connection
def establish_db_connection():
    global conn, server
    try:
        # Set up SSH tunnel
        server = SSHTunnelForwarder(
            ('starbug.cs.rit.edu', 22),
            ssh_username=username,
            ssh_password=password,
            remote_bind_address=('127.0.0.1', 5432)
        )
        server.start()
        print("SSH tunnel established")

        # Set up database connection
        params = {
            'database': dbName,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }

        conn = psycopg2.connect(**params)
        print("Database connection established")
    except Exception as e:
        print(f"Error establishing connection: {e}")
        conn = None
        server = None

# Function to retrieve the database connection (handles reconnect if needed)
def get_db_connection():
    global conn, server
    if conn is None or conn.closed != 0:
        print("Connection not established or closed. Attempting to reconnect...")
        establish_db_connection()
    return conn


def close_db_connection():
    global conn, server
    if conn:
        conn.close()
        print("Database connection closed")
    if server:
        server.stop()
        print("SSH tunnel closed")


# Usage example
if __name__ == '__main__':
    # Get database connection
    connection = get_db_connection()

    if connection:
        # Perform your DB operations here...
        print("Performing database work...")

    # Close the connection and tunnel
    close_db_connection()
