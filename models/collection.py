import psycopg2
from db import get_db_connection  # Ensure db.py is in the same directory
# AUTHOR : KIFEKACHUKWU NWOSU
conn = get_db_connection()
user_id = input("Enter your username")  # Example user ID THAT WILL NOT QORK

def printCollectionsMenu():
    while True:
        print("\nWelcome to the Collections Menu!")
        print("Here are the available commands: ")
        print("0: Reprint the collections menu")
        print("1: Create a collection")
        print("2: View a List of Your Collections")
        print("3: Delete a collection")
        print("4: Add a VideoGame to a collection")
        print("5: Delete a VideoGame from a collection")
        print("6: Modify a collection name")
        print("7: Return to the main menu")

        userinput = input("Enter the number that corresponds to your command: ").strip()
        if userinput == "0":
            printCollectionsMenu()
        elif userinput == "1":
            create_collection(user_id)
        elif userinput == "2":
            view_collections(user_id)
        elif userinput == "3":
            delete_collection(user_id)
        elif userinput == "4":
            addMovietoCollection()
        elif userinput == "5":
            delete_movie_from_collection(user_id)
        elif userinput == "6":
            modifyCollectionName(user_id)
        elif userinput == "7":
            print("Returning to the main menu...")
            break
        else:
            print("Invalid input. Try again.")


def view_collections(user_id):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT collectionname FROM collections WHERE username = %s", (user_id,))
        collections = cursor.fetchall()
        total= 0
        for i in collections:
            print(i)
        print("totak in collections :", total)
        if not collections:
            print("No collections found.")
        else:
            print("Your Collections:")
            for collection in collections:
                print(f"- {collection[0]}")
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# def print_games_in_collection(collection):
#     conn = get_db_connection()
#     if conn is None:
#         print("Failed to connect to the database.")
#         return
#     try:
#         cursor = conn.cursor()
#         cursor.execute("SELECT collectionname FROM collections WHERE username = %s", (collection,))


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

            collectionname = input("Enter a name for your collection: ").strip()\

            cursor.execute("SELECT collectionname FROM collections WHERE username = %s", (user_id,))
            collections = cursor.fetchall()
            if collectionname in collections:
                print("This collection already exists, please enter a new name")
                collectionname = input("Enter a new name for your collection: ")
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
                'SELECT "collectionid" FROM "collections" WHERE "collectionname" = %s AND "username" = %s',
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

            # cursor.execute(
            #     'DELETE FROM "contains" WHERE "collectionname" = %s',
            #     (collection_name,)
            # )
            # conn.commit()

            print(f"Collection '{collection_name}' and its associated movies have been deleted successfully.")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

def addMovietoCollection():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        collection_name = input("Enter the name of the collection you want to add a movie to: ").strip()
        while not collection_name:
            collection_name = input("The name you input was not valid. Enter the name of the collection: ").strip()

        cursor.execute("SELECT collectionid FROM collections WHERE userid = %s AND collectionname = %s",
                       (user_id, collection_name))
        collection = cursor.fetchone()
        if not collection:
            print("Collection not found.")
            return
        collection_id = collection[0]

        movie_id = None
        while movie_id is None:
            movie_name = input("Enter the name of the movie you would like to add: ").strip()
            while not movie_name:
                movie_name = input("The movie you input was not valid. Enter the name of the movie: ").strip()

            cursor.execute("SELECT movieid, mpaa_rating FROM movie WHERE title = %s", (movie_name,))
            movies = cursor.fetchall()

            if len(movies) == 1:
                movie_id = movies[0][0]
            elif len(movies) > 1:
                print("There are multiple movies with that title. Please select the correct one:")
                for m_id, rating in movies:
                    print(f"{m_id}: {movie_name}, Rating: {rating}")
                try:
                    movie_id = int(input("Enter the movie ID: ").strip())
                except ValueError:
                    print("Invalid input. Please enter a numeric movie ID.")
                    movie_id = None
            else:
                print("Movie not found in the database.")
                continue

        cursor.execute("INSERT INTO contains (collectionid, movieid) VALUES (%s, %s)", (collection_id, movie_id))
        conn.commit()
        print("Movie added successfully!")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def modifyCollectionName(user_id):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return
    try:
        old_collection_name =input("Enter the name of the collection you would like to change:");
        while not old_collection_name:
            print("The name you input was not valid.\nEnter the name of the collection you would like to change.")
            old_collection_name = input("Enter the name of the collection you would like to change:");
        new_name = input("Enter the new collection name: ")
        with conn.cursor() as cursor:
            cursor.execute("SELECT \"collectionid\" FROM \"collections\" WHERE \"collectionname\"=%s AND \"username\"=%s",
                           (old_collection_name, user_id))
            result = cursor.fetchone()
            if result is None:
                print(f"No collection found with the name '{old_collection_name}'.")
                return
            coll_id = result[0]
            cursor.execute("UPDATE \"collections\" SET \"collectionname\"=%s WHERE \"collectionid\"=%s",
                           (new_name, coll_id))
            conn.commit()
            print(f"Collection name updated successfully to '{new_name}'.")
    except psycopg2.Error as e:
        print(f"Error during database operation: {e}")
        conn.rollback()


def delete_movie_from_collection(user_id):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        collection_name = input("Enter the name of the collection you want to remove a movie from: ").strip()
        while not collection_name:
            collection_name = input("The name you input was not valid. Enter the name of the collection: ").strip()

        cursor.execute("SELECT collectionid FROM collections WHERE userid = %s AND collectionname = %s",
                       (user_id, collection_name))
        collection = cursor.fetchone()
        if not collection:
            print("Collection not found.")
            return
        collection_id = collection[0]

        movie_name = input("Enter the name of the movie you want to remove: ").strip()
        while not movie_name:
            movie_name = input("The movie you input was not valid. Enter the name of the movie: ").strip()

        cursor.execute("SELECT movieid FROM movie WHERE title = %s", (movie_name,))
        movie = cursor.fetchone()
        if not movie:
            print("Movie not found in the database.")
            return
        movie_id = movie[0]

        cursor.execute("DELETE FROM contains WHERE collectionid = %s AND movieid = %s", (collection_id, movie_id))
        conn.commit()
        print("Movie removed successfully!")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Function to reconnect to the database
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn
