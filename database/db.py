import psycopg2

# Replace these values with your actual database connection details
host = "127.0.0.1"         # The host of the database
port = "5432"              # The port (default: 5432)
dbname = "p32001_19"    # The database name
user = "knn4602"     # Your PostgreSQL username
password = "Kainakaren112$" # Your PostgreSQL password

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
    print(f"Error: {error}")
