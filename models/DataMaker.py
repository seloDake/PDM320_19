# date: 3/15/25-3/16/25
# author: Liv Jaszczak

# defining important constants and data structures
# number of rows in a primary table - our project requirements said 1000s to 10000s so we'd have enough for data analysis
primary_row_count = 15000

# maximum number of connection retries - this number is arbitrarily chosen
MAX_RETRIES = 4

# number of seconds between each connection attempt - arbitrarily chosen
TRY_DELAY = 2

# a set containing the usernames since they need to be unique
# no other user fields need to be unique
usernames = set()

# importing libraries
from faker import Faker  # This library that generates fake data
import time # so we can delay reconnect attempts
import psycopg2  # for connecting python and postgre
from psycopg2 import extras
from db import get_db_connection  # Ensure db.py is in the same directory/folder

# create a faker object and access Faker methods
fake = Faker()


# makes one random password that meets our database's criteria:
# length of at least 8
# >= 1 lower case letter
# at least 1 special char
# at least 1 digit
# @ least 1 upper case letter
def generate_password():
    password = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return password

# makes usernames, verifying they are unique first
def generate_username():
    while True:
        username = fake.user_name()
        length = len(usernames)
        usernames.add(username)
        new_length = len(usernames)
        if(new_length > length):
            return username


# Generates random data for the USERS table
def make_users_data():
    username = generate_username()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = generate_password()
    creation_date = fake.date_this_decade().strftime('%Y-%m-%d %H:%M:%S')

    return username, email, first_name, last_name, password, creation_date


# Generate PRIMARY_ROW_COUNT rows of data
def make_users_rows(primary_row_count, users_data):
    for i in range(primary_row_count):
        users_data.append(make_users_data())


# to make an attempt to reconnect the database
# originally written by KIFEKACHUKWU NWOSU in collection.py
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn


# Function to insert the created user data onto the server
def insert_users_data(users_data, MAX_RETRIES):
    # a while loop and counter so we don't keep trying to connect to the database over and over again
    attempts = 0

    while attempts < MAX_RETRIES:
        connection = get_db_connection()
        if connection is None:
            print("Couldn't't connect to the database.")
            return

        try:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO USERS (Username, Email, First_name, Last_name, Password, Creation_date) 
                VALUES %s
                """
                # a bulk insert for the more efficient insertion of 15000 rows
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

# executes the process of adding user data by calling above functions
def main():
    users_data = []

    make_users_rows(primary_row_count, users_data)
    insert_users_data(users_data, MAX_RETRIES)
