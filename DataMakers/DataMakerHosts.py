# date: 3/18/25
# author: LIV JASZCZAK

# defining important constants and data structures

# number of rows in a relation table - our project requirements said at least
# 5000 so we'd have enough for data analysis
row_count = 6000

# maximum number of connection retries - this number is arbitrarily chosen
MAX_RETRIES = 4

# number of seconds between each connection attempt - arbitrarily chosen
TRY_DELAY = 2

# min videogame id
min_videogame_id = 1
# max videogame id
max_videogame_id = 30000
# min platform id
min_platform_id = 75600
# max platform id
max_platform_id = 90599

#portion of videogames below $10
portion_1 = .15
#portion of videogames in the $10 - $60 range
portion_2 = .5
#portion of videogames in the $60 - $70 range
portion_3 = .3
#portion of videogames in the $70 - $100 range
portion_4 = .05


# importing libraries
from faker import Faker  # This library that generates fake data
import time # so we can delay reconnect attempts
import psycopg2  # for connecting python and postgre
import random
from db import get_db_connection  # Ensure db.py is in the same directory/folder
import datetime

# create a faker object and access Faker methods
fake = Faker()

# to make an attempt to reconnect the database
# originally written by KIFEKACHUKWU NWOSU in collection.py
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn

# Function to insert the created user data onto the server
def insert_hosts_data(lst, MAX_RETRIES):
    attempts = 0
    # a while loop and counter so we don't keep trying to connect to the database over and over again
    while attempts < MAX_RETRIES:
        connection = get_db_connection()
        if connection is None:
            print("Couldn't connect to the database.")
            return

        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO HOSTS (PLATFORMID, VIDEOGAMEID, RELEASE_DATE, PRICE) VALUES (%s, %s, %s, %s)"

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
    lst = []

    for i in range(1, 6000):
        platform = random.randrange(min_platform_id, max_platform_id)
        videogame = random.randrange(min_videogame_id, max_videogame_id)
        #the start date is the year of the release of the 1st ever video game
        # and the end date is the date of our last day in class
        release_date = fake.date_between(start_date=datetime.date(1958, 1, 1), end_date=datetime.date(2025, 4, 28)).strftime('%Y-%m-%d %H:%M:%S')
        bracket_picker = random.uniform(0, 1)
        if bracket_picker < portion_1:
            price = round(random.uniform(0, 10), 2)
        elif bracket_picker < (portion_1 + portion_2):
            price = round(random.uniform(10, 60), 2)
        elif bracket_picker < (portion_1 + portion_2 + portion_3):
            price = round(random.uniform(60, 70), 2)
        else:
            price = round(random.uniform(10, 60), 2)

        tuple = (platform, videogame, release_date, price)
        lst.append(tuple)

    insert_hosts_data(lst, MAX_RETRIES)

main()
