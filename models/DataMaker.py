# date: 3/15/25
# author: Liv Jaszczak

# defining important constants
PRIMARY_ROW_COUNT = 15000  # number of rows in a primary table
MAX_RETRIES = 3  # maximum number of connection retries
TRY_DELAY = 2  # number of seconds between each connection attempt

# importing libraries
from faker import Faker  # This library that generates fake data
import time
import psycopg2  # for connecting python and postgre
from psycopg2 import extras
from db import get_db_connection  # Ensure db.py is in the same directory

# create a faker object
fake = Faker()


# makes one random password that meets our criteria
def make_password():
    password = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return password


# Generates random data for the USERS table
def make_users_data():
    username = fake.user_name()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = make_password()
    creation_date = fake.date_this_decade().strftime('%Y-%m-%d %H:%M:%S')

    return username, email, first_name, last_name, password, creation_date


# Generate PRIMARY_ROW_COUNT rows of data
def make_users_rows(PRIMARY_ROW_COUNT, users_data):
    for i in range(PRIMARY_ROW_COUNT):
        users_data.append(make_users_data())


# to make an attempt to reconnect the database
# originally written by KIFEKACHUKWU NWOSU
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn


# Function to insert the created user data onto the server
def insert_users_data(users_data, MAX_RETRIES):
    # a while loop and counter so we don't keep trying to connect to the database for eternity
    attempts = 0

    while attempts < MAX_RETRIES:
        connection = get_db_connection()
        if connection is None:
            print("Couldn't't connect to the database.")
            return

        try:
            with connection.cursor() as cursor:
                # Bulk insert
                insert_query = """
                INSERT INTO USERS (Username, Email, First_name, Last_name, Password, Creation_date) 
                VALUES %s
                """
                extras.execute_values(cursor, insert_query, users_data)

                connection.commit()
                print(f"success message")
                return  # Exit on success

        # in the case of a failure to connect...
        except psycopg2.OperationalError as e:
            # print a message so the user can see what's going wrong and how many attempts are left
            print(f"Operational error: {e}. Retrying ({attempts + 1}/{MAX_RETRIES})...")
            if connection:
                connection.close()  # Close the failed connection
            time.sleep(TRY_DELAY)  # Wait before retrying to give a chance for things to fix themselves
            attempts += 1

        # announce any database errors and rollback any database edits to prevent half-way changes
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            connection.rollback()
            return  # Exit on failure
        finally:
            if connection:
                connection.close()

    #let the user know if we ran out of tries to connect to the database
    print("Max retries reached. Could not create collection.")
