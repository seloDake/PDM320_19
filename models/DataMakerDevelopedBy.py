# date: 3/19/25
# author: LIV JASZCZAK
import random

# defining important constants and data structures

# number of rows in a relation table - our project requirements said at least
# 5000 so we'd have enough for data analysis
row_count = 6000

# maximum number of connection retries - this number is arbitrarily chosen
MAX_RETRIES = 4

# number of seconds between each connection attempt - arbitrarily chosen
TRY_DELAY = 2

#min game id
min_game_id = 1

#max gameid
max_game_id = 30000

#min dev id
min_dev_id = 1

#max dev id
max_dev_id = 15000

#dev amount ranges. There are 5 categories of dev amounts
dev_count_ranges = [[1,3], [2, 10], [10,30], [30,50], [50,100]]

# importing libraries
from faker import Faker  # This library that generates fake data
import time # so we can delay reconnect attempts
import psycopg2  # for connecting python and postgre
from db import get_db_connection  # Ensure db.py is in the same directory/folder

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

# generates the data
def make_data():
    data = set() #we're using a set to prevent duplicate values
    while(len(data) < row_count):
        game_id = random.randrange(1, max_game_id + 1)
        category = random.randrange(0, 5)
        min_dev_amount = dev_count_ranges[category][0]
        max_dev_amount = dev_count_ranges[category][1]+1
        dev_amount = random.randrange(min_dev_amount, max_dev_amount)
        print(dev_amount)
        for i in range(dev_amount):
            dev_id = random.randrange(min_dev_id+1, max_dev_id+1, 2)#let's say devs have even ids
            data.add((dev_id, game_id))
    return list(data)

# Function to insert the created user data onto the server
def insert_data(data, MAX_RETRIES):
    # a while loop and counter so we don't keep trying to connect to the database over and over again
    attempts = 0

    while attempts < MAX_RETRIES:
        connection = get_db_connection()
        if connection is None:
            print("Couldn't connect to the database.")
            return

        try:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO DEVELOPED_BY (makerid, videogameid) VALUES (%s, %s) """
                # Individually insert each item in the list of genre names
                for item in data:
                    item_list = (item)
                    cursor.execute(insert_query, (item_list[0], item_list[1]))

                connection.commit()
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
            return  # Exit on failure
        finally:
            if connection:
                connection.close()

    #let the user know if we ran out of tries to connect to the database
    print("Max retries reached. Could not create collection.")

# executes the process of adding user data by calling above functions
def main():
    data = make_data()

    insert_data(data, MAX_RETRIES)
    print("Hi there.")

main()
