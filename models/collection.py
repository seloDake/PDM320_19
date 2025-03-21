import psycopg2
from db import get_db_connection # Ensure db.py is in the same directory
import user
# AUTHOR : KIFEKACHUKWU NWOSU
conn = get_db_connection()
# user_id = input("Enter your username")  # Example user ID THAT WILL NOT QORK


def printCollectionsMenu(user_id):
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
            addVideoGametoCollection()
        elif userinput == "5":
            delete_vidoeGame_from_collection(user_id)
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

        # Get all collections with game counts
        cursor.execute("""
            SELECT c.collectionid, c.collectionname, COUNT(co.videogameid) 
            FROM collections c
            LEFT JOIN contains co ON c.collectionid = co.collectionid
            WHERE c.username = %s
            GROUP BY c.collectionid, c.collectionname
            ORDER BY c.collectionname;
        """, (user_id,))

        collections = cursor.fetchall()

        if not collections:
            print("No collections found.")
        else:
            print("Your Collections:")
            for collection_id, collection_name, game_count in collections:
                print(f"\n📂 {collection_name} ({game_count} games)")

                # Fetch video games for this collection
                cursor.execute("""
                    SELECT v.title 
                    FROM contains co
                    JOIN videogame v ON co.videogameid = v.videogameid
                    WHERE co.collectionid = %s
                    ORDER BY v.title;
                """, (collection_id,))

                games = cursor.fetchall()

                if games:
                    for game in games:
                        print(f"{game[0]}")
                else:
                    print("No games in this collection.")

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

            cursor.execute("SELECT collectionname FROM collections WHERE username = %s", (username,))
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

            print(f"Collection '{collection_name}' and its associated movies have been deleted successfully.")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

def addVideoGametoCollection(user_id):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        collection_name = input("Enter the name of the collection you want to add a VideoGame to: ").strip()
        while not collection_name:
            collection_name = input("The name you input was not valid. Enter the name of the collection: ").strip()

        cursor.execute("SELECT collectionid FROM collections WHERE username = %s AND collectionname = %s",
                       (user_id, collection_name))
        collection = cursor.fetchone()
        if not collection:
            print("Collection not found.")
            return
        collection_id = collection[0]

        game_id = None
        while game_id is None:
            game_name = input("Enter the name of the VideoGame you would like to add: ").strip()
            while not game_name:
                game_name = input("The Video Game you input was not valid. Enter the name of the Video Game: ").strip()

            cursor.execute("SELECT videogameid, esrb_rating FROM videogame WHERE title = %s", (game_name,))
            videogames = cursor.fetchall()

            if len(videogames) == 1:
                game_id = videogames[0][0]
            elif len(videogames) > 1:
                print("There are multiple videogames with that title. Please select the correct one:")
                for m_id, rating in videogames:
                    print(f"{m_id}: {game_name}, Rating: {rating}")
                try:
                    game_id = int(input("Enter the Videogame ID: ").strip())
                except ValueError:
                    print("Invalid input. Please enter a numeric VideoGame ID.")
                    game_id = None
            else:
                print("VideoGame not found in the database.")
                continue

        cursor.execute("INSERT INTO contains (collectionid, videogameid, username) VALUES (%s, %s, %s)", (collection_id, game_id, user_id))
        conn.commit()
        print("Game added successfully!")

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


def delete_vidoeGame_from_collection(user_id):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        collection_name = input("Enter the name of the collection you want to remove a VideoGame from: ").strip()
        while not collection_name:
            collection_name = input("The name you input was not valid. Enter the name of the collection: ").strip()

        cursor.execute(
            'SELECT "collectionid" FROM "collections" WHERE "collectionname" = %s AND "username" = %s',
            (collection_name, user_id)
        )
        collection = cursor.fetchone()
        if not collection:
            print("Collection not found.")
            return
        collection_id = collection[0]

        videogame_name = input("Enter the name of the VideoGame you want to remove: ").strip()
        while not videogame_name:
            videogame_name = input("The VideoGame you input was not valid. Enter the name of the VideoGame: ").strip()

        cursor.execute("SELECT videogameid FROM videogame WHERE title = %s", (videogame_name,))
        videogame = cursor.fetchone()
        if not videogame:
            print("Videogame not found in the database.")
            return
        game_id = videogame[0]

        cursor.execute("DELETE FROM contains WHERE collectionid = %s AND videogameid = %s", (collection_id, game_id))
        conn.commit()
        print("Videogame removed successfully!")
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
