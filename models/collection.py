import psycopg2
from db import get_db_connection  # Ensure db.py is in the same directory
# AUTHOR : KIFEKACHUKWU NWOSU
conn = get_db_connection()
user_id = 3  # Example user ID THAT WILL NOT QORK

def printCollectionsMenu():
    while True:
        print("\nWelcome to the Collections Menu!")
        print("Here are the available commands: ")
        print("0: Reprint the collections menu")
        print("1: Create a collection")
        print("2: View a List of Your Collections")
        print("3: Delete a collection")
        print("4: Add a movie to a collection")
        print("5: Delete a movie from a collection")
        print("6: Modify collection")
        print("7: Return to the main menu")

        userinput = input("Enter the number that corresponds to your command: ").strip()

        if userinput == "1":
            create_collection(user_id)
        elif userinput == "3":
            delete_collection(user_id)
        elif userinput == "7":
            print("Returning to the main menu...")
            break  # Exits the loop and returns to main.py
        else:
            print("Invalid input. Try again.")


# Function to create a collection
def create_collection(username):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT MAX("collectionid") FROM "collections"')
            max_id = cursor.fetchone()[0] or 0

            # Increment the max id by 1
            new_collection_id = max_id + 1

            collectionname = input("Enter a name for your collection: ").strip()
            if not collectionname:
                collectionname = "Collection"

            cursor.execute(
                'INSERT INTO "collections" ("collectionid", "username", "collectionname") VALUES (%s, %s, %s)',
                (new_collection_id, username, collectionname)
            )
            conn.commit()
            print("Collection created successfully!")

    except psycopg2.OperationalError as e:
        print(f"Operational error: {e}. Trying to reconnect...")
        conn = reconnect_db()
        if conn:
            create_collection(username)
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

def delete_collection(user_id):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        # Step 1: Ask the user to enter the collection name they want to delete
        collection_name = input("Enter the name of the collection you would like to delete: ").strip()

        # Step 2: Find the collection ID corresponding to the collection name and user ID
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT "collectionid" FROM "collections" WHERE "collectionname" = %s AND "userid" = %s',
                (collection_name, user_id)
            )
            result = cursor.fetchone()

            if result is None:
                print(f"No collection found with the name '{collection_name}'.")
                return

            collection_id = result[0]
            cursor.execute(
                'DELETE FROM "collections" WHERE "collectionid" = %s',
                (collection_id,)
            )
            conn.commit()

            cursor.execute(
                'DELETE FROM "contains" WHERE "collectionid" = %s',
                (collection_id,)
            )
            conn.commit()

            print(f"Collection '{collection_name}' and its associated movies have been deleted successfully.")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()


# Function to reconnect to the database
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn
