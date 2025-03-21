# date: 3/19/25
# author: LIV JASZCZAK

# defining important constants and data structures

# number of rows in a relation table - our project requirements said at least
# 5000 so we'd have enough for data analysis
row_count = 6000

# maximum number of connection retries - this number is arbitrarily chosen
MAX_RETRIES = 4

# number of seconds between each connection attempt - arbitrarily chosen
TRY_DELAY = 2

# importing libraries
import time # so we can delay reconnect attempts
import psycopg2  # for connecting python and postgre
from db import get_db_connection  # Ensure db.py is in the same directory/folder

# to make an attempt to reconnect the database
# originally written by KIFEKACHUKWU NWOSU in collection.py
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn

# Function to insert the created user data onto the server
def insert_data(lst, MAX_RETRIES):
    attempts = 0
    # a while loop and counter so we don't keep trying to connect to the database over and over again
    while attempts < MAX_RETRIES:
        connection = get_db_connection()
        if connection is None:
            print("Couldn't connect to the database.")
            return

        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO PLAYS (USERNAME, VIDEOGAMEID, SESSION_START, SESSION_END) VALUES (%s, %s, %s, %s)"

                # inserting the items individually bc I could not get a bulk insert to work
                for item in lst:
                    cursor.execute(insert_query, (item[0], item[1], item[2], item[3]))

                connection.commit()  # Commit once after all inserts
                print(f"Data Committed")
                return  # Exit on success

        # in the case of a failure to connect...
        except psycopg2.OperationalError as e:
            # print a message so the user can see what's going wrong and how many attempts are left
            print(f"Operational error: {e}. Retrying ({attempts + 1}/{MAX_RETRIES})...")
            if connection:
                connection.close()
            time.sleep(TRY_DELAY)
            attempts += 1

        # announce any database errors and rollback any database edits to prevent half-way changes
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            connection.rollback()
            return

        finally:
            if connection:
                connection.close()

    #let the user know if we ran out of tries to connect to the database
    print("Max retries reached. Could not create collection.")


# executes the process of adding user data by calling above functions
def main():
    follow_lst = []

    # The pairs in follows come from ChatGPT pairing users
    with open('plays') as file:
        for line in file:
            print(line)
            print(tuple(line.strip().split("|")))
            follow_lst.append(tuple(line.strip().split("|")))

    insert_data(follow_lst, MAX_RETRIES)

main()
