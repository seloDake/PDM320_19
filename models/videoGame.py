import datetime
import psycopg2
from db import get_db_connection # Ensure db.py is in the same directory
from datetime import date
import user

# AUTHOR : Christabel Osei
# Author : Kiffy Nwosu
# AUTHOR : Selorm Dake
conn = get_db_connection()

def printVideoGamesMenu(username):
    while True:
        print("\nWelcome to the VideoGames Menu!")
        print("Here are the available commands: ")
        print("0: Reprint the collections menu")
        print("1: Play a video game")
        print("2: Search for a video game")
        print("3: Play a random video game")
        print("4: View your top videogames")
        print("4: Return to the main menu")

        userinput = input("Enter the number that corresponds to your command: ").strip()
        if userinput == "0":
            printVideoGamesMenu(username)
        elif userinput == "1":
            play_video_game(username,conn)
        elif userinput == "2":
            videogame_search_menu()
        elif userinput == "3":
            play_random_game(username,conn)
        elif userinput == "4":
            top_10_user_games(username)
            break
        elif userinput == "5":
            print("Returning to the main menu...")
            break
        else:
            print("Invalid input. Try again.")

def play_video_game(username, conn):
    """Logs when a user starts and ends playing a video game."""
    game_name = input("Enter the name of the video game you want to play: ").strip()
    with conn.cursor() as cursor:
        # Check if the game exists in the database.
        cursor.execute(
            'SELECT "videogameid" FROM "videogame" WHERE title = %s',
            (game_name,)
        )
        result = cursor.fetchone()
        if not result:
            print("Game not found.")
            return
        game_id = result[0]

        # Log the start time.
        start_time = datetime.datetime.now()
        print(f"You started playing {game_name} at {start_time}.")
        input("Press Enter to stop playing...")

        # Log the end time and calculate play duration in minutes.
        end_time = datetime.datetime.now()
        play_time = (end_time - start_time).total_seconds() // 60

        # Insert the play session into the database.
        cursor.execute("""
            INSERT INTO plays (username, videogameid, session_start, session_end)
            VALUES (%s, %s, %s, %s)
        """, (username, game_id, start_time, end_time))
        conn.commit()
        print(f"You played {game_name} for {play_time} minutes. Would you like to rate it?\n")
        userinput = input("Enter yes or no: ").strip()
        if userinput == "yes":
            rate_video_game(username, conn)
        elif userinput == "no":
            print("Thank you for playing!")
            printVideoGamesMenu(username)
        
def videogame_search_menu():
    while True:
        print("🔍 What would you like to search by?")
        print("1️⃣: VideoGame Name 🎮")
        print("2️⃣: VideoGame Release Date 📅")
        print("3️⃣: Platform 🖥️🎮")
        print("4️⃣: Genre 🏷️")
        print("5️⃣: Price 💰")
        print("6️⃣: Reprint these options 🔄")
        print("7️⃣: Return to main menu 🔙")

        searchby = input("🔍 What would you like to search by? ")
        if searchby == "1":
            search_video_games_by_name()
        elif searchby == "2":
            search_video_games_by_release_date(conn)
        elif searchby == "3":
            search_video_games_by_platform()
        elif searchby == "4":
            search_video_games_by_genre()
        elif searchby == "5":
            search_video_games_by_price()
        elif searchby == "6":
            videogame_search_menu()
        elif searchby == "7":
            break
        else:
            print("❌❌Invalid Input try again")
def sorting_options():
    sorting_options = {
            "1": "v.title ASC, h.release_date ASC",   # Default (name, release date)
            "2": "v.title DESC, h.release_date DESC", # Name (descending)
            "3": "h.price ASC",
            "4": "h.price DESC", # Price (descending)
            "5": "g.genrename ASC", # Genre (ascending)
            "6": "g.genrename DESC", # Genre (descending)
            "7": "h.release_date ASC", # Release year (ascending)
            "8": "h.release_date DESC" # Release year (descending)
        }

    print("\n📌 Sorting Options:")
    print("   1️⃣. Name & Release Date (Ascending) [Default] 🔼")
    print("   2️⃣. Name & Release Date (Descending) 🔽")
    print("   3️⃣. Price (Ascending) 💰🔼")
    print("   4️⃣. Price (Descending) 💰🔽")
    print("   5️⃣. Genre (Ascending) 🏷️🔼")
    print("   6️⃣. Genre (Descending) 🏷️🔽")
    print("   7️⃣. Release Year (Ascending) 📅🔼")
    print("   8️⃣. Release Year (Descending) 📅🔽")
    print("   9.Change the search order")


    sort_choice = input("Choose a sorting option (1-8): ").strip()
    sort_query = sorting_options.get(sort_choice, "v.title ASC, h.release_date ASC")


def search_video_games_by_name():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        name = input("Please enter the name of the Video Game you would like to search for: ").strip()
        if not name:
            print("❌ Invalid input. Please enter a valid video game name.")
            return

        # Sorting options
        sorting_options = {
            "1": "v.title ASC, h.release_date ASC",   # Default (name, release date)
            "2": "v.title DESC, h.release_date DESC", # Name (descending)
            "3": "h.price ASC",
            "4": "h.price DESC", # Price (descending)
            "5": "g.genrename ASC", # Genre (ascending)
            "6": "g.genrename DESC", # Genre (descending)
            "7": "h.release_date ASC", # Release year (ascending)
            "8": "h.release_date DESC" # Release year (descending)
        }

        print("\n📌 Sorting Options:")
        print("   1️⃣. Name & Release Date (Ascending) [Default] 🔼")
        print("   2️⃣. Name & Release Date (Descending) 🔽")
        print("   3️⃣. Price (Ascending) 💰🔼")
        print("   4️⃣. Price (fDescending) 💰🔽")
        print("   5️⃣. Genre (Ascending) 🏷️🔼")
        print("   6️⃣. Genre (Descending) 🏷️🔽")
        print("   7️⃣. Release Year (Ascending) 📅🔼")
        print("   8️⃣. Release Year (Descending) 📅🔽")
        print("   9.Change the search order")


        sort_choice = input("Choose a sorting option (1-8): ").strip()
        sort_query = sorting_options.get(sort_choice, "v.title ASC, h.release_date ASC")  # Default sorting

        print(f"🔍 Searching for '{name}', sorted by chosen criteria...\n")

        query = f"""
    SELECT v.title,
       v.esrb_rating,
       h.release_date,
       h.price,
       p.name AS platform_name,
       COALESCE(array_agg(DISTINCT g.genrename), ARRAY[]::TEXT[]) AS genres,
        COALESCE(STRING_AGG(DISTINCT m.makername, ', '), 'Unknown') AS publishers
        FROM videogame v
        JOIN hosts h ON v.videogameid = h.videogameid
        JOIN platform p ON h.platformid = p.platformid
        JOIN game_is_genre gg ON v.videogameid = gg.videogameid
        JOIN genre g ON gg.genreid = g.genreid
        LEFT JOIN published_by pb ON v.videogameid = pb.videogameid
        LEFT JOIN maker m ON pb.makerid = m.makerid
        WHERE v.title ILIKE %s
        GROUP BY v.videogameid, h.release_date, h.price, p.name
        ORDER BY {sort_query}; 

        """

        with conn.cursor() as cursor:
            cursor.execute(query, (f"%{name}%",))
            result_set = cursor.fetchall()

        if not result_set:
            print("❌ No games found with that name.")
            return

        print("\n🎮 Video Games Found:")
        for row in result_set:
            title, esrb_rating, release_date, price, platform, genres, makers = row
            genres = genres or []  # Ensure it's always a list
            makers = makers.split(', ') if makers and makers != 'Unknown' else ["Unknown"]

            print(f"   📌 {title} | ESRB: {esrb_rating} | Released: {release_date} | Price: ${price:.2f}")
            print(f"      🎮 Platform: {platform}")
            print(f"      🎭 Genres: {', '.join(genres) if genres else 'N/A'}")


    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

def search_video_games_by_price():
    conn = get_db_connection()  # Ensure a valid DB connection
    if conn is None:
        print("❌ Failed to connect to the database.")
        return

    try:
        min_price = float(input("Enter the minimum price: ").strip())
        max_price = float(input("Enter the maximum price: ").strip())

        if min_price > max_price:
            print("❌ Invalid range. The minimum price cannot be greater than the maximum price.")
            return

        print(f"\n🔍 Searching for games priced between ${min_price:.2f} and ${max_price:.2f}...\n")

        # Default sorting (Alphabetically by game name, then release date)
        order_by_clause = "ORDER BY v.title ASC, h.release_date ASC"

        print("\n📌 Sorting Options:")
        print("   1️⃣. Name & Release Date (Ascending) [Default] 🔼")
        print("   2️⃣. Name & Release Date (Descending) 🔽")
        print("   3️⃣. Price (Ascending) 💰🔼")
        print("   4️⃣. Price (Descending) 💰🔽")
        print("   5️⃣. Genre (Ascending) 🏷️🔼")
        print("   6️⃣. Genre (Descending) 🏷️🔽")
        print("   7️⃣. Release Year (Ascending) 📅🔼")
        print("   8️⃣. Release Year (Descending) 📅🔽")

        user_sort_option = input("Choose an option (1-6): ").strip()

        sort_options = {
            "1": "v.title ASC, h.release_date ASC",
            "2": "v.title DESC, h.release_date DESC",
            "3": "h.price ASC",
            "4": "h.price DESC",
            "5": "EXTRACT(YEAR FROM h.release_date) ASC",
            "6": "EXTRACT(YEAR FROM h.release_date) DESC"
        }

        if user_sort_option in sort_options:
            order_by_clause = f"ORDER BY {sort_options[user_sort_option]}"

        query = f"""
            SELECT v.title,
                   v.esrb_rating,
                   h.release_date,
                   h.price,
                   p.name AS platform,
                   COALESCE(array_agg(DISTINCT g.genrename), '{{}}') AS genres,
                   COALESCE(array_agg(DISTINCT m.name), '{{}}') AS makers
            FROM videogame v
            JOIN hosts h ON v.videogameid = h.videogameid
            JOIN platform p ON h.platformid = p.platformid
            JOIN game_is_genre gg ON v.videogameid = gg.videogameid
            JOIN genre g ON gg.genreid = g.genreid
            JOIN published_by pb ON p.platformid = pb.platformid  -- Get makerid from platform
            JOIN maker m ON pb.makerid = m.makerid  -- Get maker name
            WHERE h.price BETWEEN %s AND %s
            GROUP BY v.videogameid, h.release_date, h.price, p.name
            {order_by_clause};
        """

        with conn.cursor() as cursor:
            cursor.execute(query, (min_price, max_price))
            result_set = cursor.fetchall()

        if not result_set:
            print(f"❌ No games found in the price range ${min_price:.2f} - ${max_price:.2f}.")
            return

        print(f"\n🎮 Video Games Priced Between ${min_price:.2f} - ${max_price:.2f}:")
        for row in result_set:
            title, esrb_rating, release_date, price, platform, genres, makers = row
            genres = genres or []
            makers = makers or []

            print(f"   📌 {title} | ESRB: {esrb_rating} | Released: {release_date} | Price: ${price:.2f}")
            print(f"      🎮 Platform: {platform}")
            print(f"      🎭 Genres: {', '.join(genres) if genres else 'N/A'}")
            print(f"      🏢 Maker(s): {', '.join(makers) if makers else 'N/A'}")

    except ValueError:
        print("❌ Invalid input. Please enter a valid number for price.")
    except psycopg2.DatabaseError as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()


import psycopg2
from datetime import date

def search_video_games_by_release_date(conn):
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()

        print("📅 Do you want to search by:\n1️⃣. Month\n2️⃣. Year\n3️⃣. Exact Date")
        search_option = input("Choose an option (1/2/3): ").strip()

        query = ""
        query_param = None

        if search_option == "1":  # Search by Month
            month = int(input("Enter the month as a number (e.g., October = 10): ").strip())
            query = "WHERE EXTRACT(MONTH FROM h.release_date) = %s"
            query_param = (month,)

        elif search_option == "2":  # Search by Year
            year = int(input("Enter the year: ").strip())
            query = "WHERE EXTRACT(YEAR FROM h.release_date) = %s"
            query_param = (year,)

        elif search_option == "3":  # Search by Exact Date
            year = int(input("Enter the year: ").strip())
            month = int(input("Enter the month: ").strip())
            day = int(input("Enter the day: ").strip())
            release_date = date(year, month, day)
            query = "WHERE h.release_date = %s"
            query_param = (release_date,)

        else:
            print("❌ Not a valid option. Please choose 1, 2, or 3.")
            return

        # Sorting options
        sorting_options = {
            "1": "v.title ASC, h.release_date ASC",  # Default (name, release date)
            "2": "v.title DESC, h.release_date DESC",
            "3": "h.price ASC",
            "4": "h.price DESC",
            "5": "g.genrename ASC",
            "6": "g.genrename DESC",
            "7": "h.release_date ASC",
            "8": "h.release_date DESC"
        }

        print("\n📌 Sorting Options:")
        print("   1️⃣. Name & Release Date (Ascending) [Default] 🔼")
        print("   2️⃣. Name & Release Date (Descending) 🔽")
        print("   3️⃣. Price (Ascending) 💰🔼")
        print("   4️⃣. Price (Descending) 💰🔽")
        print("   5️⃣. Genre (Ascending) 🏷️🔼")
        print("   6️⃣. Genre (Descending) 🏷️🔽")
        print("   7️⃣. Release Year (Ascending) 📅🔼")
        print("   8️⃣. Release Year (Descending) 📅🔽")

        sort_choice = input("Choose a sorting option (1-8): ").strip()
        sort_query = sorting_options.get(sort_choice, "v.title ASC, h.release_date ASC")  # Default sorting

        full_query = f"""
            SELECT v.title,
                   v.esrb_rating,
                   h.release_date,
                   h.price,
                   p.name AS platform_name,
                   COALESCE(array_agg(DISTINCT g.genrename), ARRAY[]::TEXT[]) AS genres
            FROM videogame v
            JOIN hosts h ON v.videogameid = h.videogameid
            JOIN platform p ON h.platformid = p.platformid
            JOIN game_is_genre gg ON v.videogameid = gg.videogameid
            JOIN genre g ON gg.genreid = g.genreid
            {query}
            GROUP BY v.videogameid, h.release_date, h.price, p.name
            ORDER BY {sort_query};
        """

        cursor.execute(full_query, query_param)
        result_set = cursor.fetchall()

        if not result_set:
            print("❌ No video games found for the selected date.")
            return

        print("\n🎮 Video Games Released on Selected Date:")
        for row in result_set:
            title, esrb_rating, release_date, price, platform, genres = row
            genres = genres or []
            print(f"   📌 {title} | ESRB: {esrb_rating} | Released: {release_date} | Price: ${price:.2f}")
            print(f"      🎮 Platform: {platform}")
            print(f"      🎭 Genres: {', '.join(genres) if genres else 'N/A'}")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()



def search_video_games_by_genre():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        genre_name = input("Please enter the genre you would like to search for: ").strip()
        if not genre_name:
            print("❌ Invalid input. Please enter a valid genre name.")
            return

        # Sorting options
        sorting_options = {
            "1": "v.title ASC, h.release_date ASC",   # Default (name, release date)
            "2": "v.title DESC, h.release_date DESC", # Name (descending)
            "3": "h.price ASC",
            "4": "h.price DESC", # Price (descending)
            "5": "h.release_date ASC", # Release year (ascending)
            "6": "h.release_date DESC" # Release year (descending)
        }

        print("\n📌 Sorting Options:")
        print("   1️⃣. Name & Release Date (Ascending) [Default] 🔼")
        print("   2️⃣. Name & Release Date (Descending) 🔽")
        print("   3️⃣. Price (Ascending) 💰🔼")
        print("   4️⃣. Price (Descending) 💰🔽")
        print("   5️⃣. Release Year (Ascending) 📅🔼")
        print("   6️⃣. Release Year (Descending) 📅🔽")

        sort_choice = input("Choose a sorting option (1-6): ").strip()
        sort_query = sorting_options.get(sort_choice, "v.title ASC, h.release_date ASC")  # Default sorting

        print(f"🔍 Searching for games in the '{genre_name}' genre, sorted by chosen criteria...\n")

        query = f"""
            SELECT v.title,
                   v.esrb_rating,
                   h.release_date,
                   h.price,
                   p.name AS platform_name,
                   COALESCE(array_agg(DISTINCT g.genrename), ARRAY[]::TEXT[]) AS genres
            FROM videogame v
            JOIN hosts h ON v.videogameid = h.videogameid
            JOIN platform p ON h.platformid = p.platformid
            JOIN game_is_genre gg ON v.videogameid = gg.videogameid
            JOIN genre g ON gg.genreid = g.genreid
            WHERE g.genrename ILIKE %s
            GROUP BY v.videogameid, h.release_date, h.price, p.name
            ORDER BY {sort_query};
        """

        with conn.cursor() as cursor:
            cursor.execute(query, (f"%{genre_name}%",))
            result_set = cursor.fetchall()

        if not result_set:
            print(f"❌ No games found in the '{genre_name}' genre.")
            return

        print(f"\n🎮 Video Games in the '{genre_name}' Genre:")
        for row in result_set:
            title, esrb_rating, release_date, price, platform, genres = row
            genres = genres or []  # Ensure it's always a list
            print(f"   📌 {title} | ESRB: {esrb_rating} | Released: {release_date} | Price: ${price:.2f}")
            print(f"      🎮 Platform: {platform}")
            print(f"      🎭 Genres: {', '.join(genres) if genres else 'N/A'}")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()


def search_video_games_by_platform():
    conn = get_db_connection()  # Ensure a valid DB connection
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        platform_name = input("Please enter the platform you would like to search for: ").strip()
        if not platform_name:
            print("❌ Invalid input. Please enter a valid platform name.")
            return

        print(f"🔍 Searching for games available on '{platform_name}', sorted alphabetically...\n")

        # Default sorting (Game Name → Release Date Ascending)
        order_by_clause = "ORDER BY v.title ASC, h.release_date ASC"

        print("\n📌 Sorting Options:")
        print("   1️⃣. Name & Release Date (Ascending) [Default] 🔼")
        print("   2️⃣. Name & Release Date (Descending) 🔽")
        print("   3️⃣. Price (Ascending) 💰🔼")
        print("   4️⃣. Price (Descending) 💰🔽")
        print("   5️⃣. Genre (Ascending) 🏷️🔼")
        print("   6️⃣. Genre (Descending) 🏷️🔽")
        print("   7️⃣. Release Year (Ascending) 📅🔼")
        print("   8️⃣. Release Year (Descending) 📅🔽")

        user_sort_option = input("Choose an option (1-6): ").strip()

        sort_options = {
            "1": "v.title ASC, h.release_date ASC",
            "2": "v.title DESC, h.release_date DESC",
            "3": "h.price ASC",
            "4": "h.price DESC",
            "5": "EXTRACT(YEAR FROM h.release_date) ASC",
            "6": "EXTRACT(YEAR FROM h.release_date) DESC"
        }

        if user_sort_option in sort_options:
            order_by_clause = f"ORDER BY {sort_options[user_sort_option]}"

        query = f"""
            SELECT v.title,
                   v.esrb_rating,
                   h.release_date,
                   h.price,
                   p.name,
                   COALESCE(array_agg(DISTINCT g.genrename), '{{}}') AS genres
            FROM videogame v
            JOIN hosts h ON v.videogameid = h.videogameid
            JOIN platform p ON h.platformid = p.platformid
            JOIN game_is_genre gg ON v.videogameid = gg.videogameid
            JOIN genre g ON gg.genreid = g.genreid
            WHERE p.name ILIKE %s
            GROUP BY v.videogameid, h.release_date, h.price, p.name
            {order_by_clause};
        """

        with conn.cursor() as cursor:
            cursor.execute(query, (f"%{platform_name}%",))
            result_set = cursor.fetchall()

        if not result_set:
            print(f"❌ No games found for the platform '{platform_name}'.")
            return

        print(f"\n🎮 Video Games Available on {platform_name}:")
        for row in result_set:
            title, esrb_rating, release_date, price, platform, genres = row
            genres = genres or []
            print(f"      🎮 Platform: {platform}")
            print(f"   📌 {title} | ESRB: {esrb_rating} | Released: {release_date} | Price: ${price:.2f}")
            print(f"      🎭 Genres: {', '.join(genres) if genres else 'N/A'}")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()



def search_video_games_by_price():
    conn = get_db_connection()  # Ensure a valid DB connection
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        min_price = float(input("Enter the minimum price: ").strip())
        max_price = float(input("Enter the maximum price: ").strip())

        if min_price > max_price:
            print("❌ Invalid range. The minimum price cannot be greater than the maximum price.")
            return

        print(f"🔍 Searching for games priced between ${min_price:.2f} and ${max_price:.2f}...\n")

        # Default sorting (Alphabetically by game name, then release date)
        order_by_clause = "ORDER BY v.title ASC, h.release_date ASC"

        print("\n📌 Sorting Options:")
        print("   1️⃣. Name & Release Date (Ascending) [Default] 🔼")
        print("   2️⃣. Name & Release Date (Descending) 🔽")
        print("   3️⃣. Price (Ascending) 💰🔼")
        print("   4️⃣. Price (Descending) 💰🔽")
        print("   5️⃣. Genre (Ascending) 🏷️🔼")
        print("   6️⃣. Genre (Descending) 🏷️🔽")
        print("   7️⃣. Release Year (Ascending) 📅🔼")
        print("   8️⃣. Release Year (Descending) 📅🔽")

        user_sort_option = input("Choose an option (1-6): ").strip()

        sort_options = {
            "1": "v.title ASC, h.release_date ASC",
            "2": "v.title DESC, h.release_date DESC",
            "3": "h.price ASC",
            "4": "h.price DESC",
            "5": "EXTRACT(YEAR FROM h.release_date) ASC",
            "6": "EXTRACT(YEAR FROM h.release_date) DESC"
        }

        if user_sort_option in sort_options:
            order_by_clause = f"ORDER BY {sort_options[user_sort_option]}"

        query = f"""
            SELECT v.title,
                   v.esrb_rating,
                   h.release_date,
                   h.price,
                   p.name,
                   COALESCE(array_agg(DISTINCT g.genrename), '{{}}') AS genres
            FROM videogame v
            JOIN hosts h ON v.videogameid = h.videogameid
            JOIN platform p ON h.platformid = p.platformid
            JOIN game_is_genre gg ON v.videogameid = gg.videogameid
            JOIN genre g ON gg.genreid = g.genreid
            WHERE h.price BETWEEN %s AND %s
            GROUP BY v.videogameid, h.release_date, h.price, p.name
            {order_by_clause};
        """

        with conn.cursor() as cursor:
            cursor.execute(query, (min_price, max_price))
            result_set = cursor.fetchall()

        if not result_set:
            print(f"❌ No games found in the price range ${min_price:.2f} - ${max_price:.2f}.")
            return

        print(f"\n🎮 Video Games Priced Between ${min_price:.2f} - ${max_price:.2f}:")
        for row in result_set:
            title, esrb_rating, release_date, price, platform, genres = row
            genres = genres or []  # Ensure it's always a list
            print(f"   📌 {title} | ESRB: {esrb_rating} | Released: {release_date} | Price: ${price:.2f}")
            print(f"      🎮 Platform: {platform}")
            print(f"      🎭 Genres: {', '.join(genres) if genres else 'N/A'}")

    except ValueError:
        print("❌ Invalid input. Please enter a valid number for price.")
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

def print_result(result_set):
    for row in result_set:
        print(row)

def rate_video_game(username, conn):
    """Allows users to rate a video game with a star rating (1-5)."""
    game_name = input("Enter the name of the video game you want to rate: ").strip()
    with conn.cursor() as cursor:
        cursor.execute('SELECT "videogameid" FROM "videogame" WHERE title = %s', (game_name,))
        result = cursor.fetchone()
        if not result:
            print("Game not found.")
            return
        game_id = result[0]
        # Check if the user has already rated this game
        cursor.execute("SELECT rating FROM rates WHERE username = %s AND videogameid = %s", (username, game_id))
        existing_rating = cursor.fetchone()
        if existing_rating:
            print(f"You have already rated this game with {existing_rating[0]} stars.")
            printVideoGamesMenu(username)  
        else:
            while True:
                try:
                    rating = int(input("Enter your star rating (1-5): ").strip())
                    if 1 <= rating <= 5:
                        break
                    else:
                        print("Please enter a number between 1 and 5.") 
                except ValueError:
                    print(" Invalid input. Please enter a number between 1 and 5.")
        cursor.execute("""
            INSERT INTO rates (username, videogameid, rating)
            VALUES (%s, %s, %s) """,(username, game_id, rating))
        conn.commit()
        print(f" You rated {game_name} with {rating} stars.")


def play_random_game(username, conn):
    """Allows the user to play a random game from their collection and logs play time."""

    with conn.cursor() as cursor:
        # Select a random game from the user's collection.
        cursor.execute('''
            SELECT vg.title, vg.videogameid FROM videogame vg
            JOIN contains uc ON vg.videogameid = uc.videogameid
            WHERE uc.username = %s
            ORDER BY RANDOM() LIMIT 1
        ''', (username,))
        result = cursor.fetchone()
        if not result:
            print("⚠️ You have no games in your collection to play.")
            return
        
        game_name, game_id = result
        
        # Log the start time of the play session.
        start_time = datetime.datetime.now()
        print(f"You started playing {game_name} at {start_time}.")
        input("Press Enter to stop playing...")
        
        # Log the end time and calculate the total play time in minutes.
        end_time = datetime.datetime.now()
        play_time = (end_time - start_time).total_seconds() // 60
        
        # Insert the play session into the database.
        cursor.execute("""
            INSERT INTO plays (username, videogameid, session_start, session_end)
            VALUES (%s, %s, %s, %s)
        """, (username, game_id, start_time, end_time))
        conn.commit()
        print(f"You played {game_name} for {play_time} minutes. Would you like to rate it?\n")
        userinput = input("Enter yes or no: ").strip()
        if userinput == "yes":
            rate_video_game(username, conn)
        elif userinput == "no":
            print("Thank you for playing!")
            printVideoGamesMenu(username)


def top_10_user_games(username):
    conn = get_db_connection()
    if conn is None:
        print("❌ Failed to connect to the database.")
        return

    print("\n📊 How would you like to rank your top 10 games?")
    print("1️⃣: By Highest Rating ⭐")
    print("2️⃣: By Most Playtime ⏱️")
    print("3️⃣: Combination of Rating & Playtime 🥇")

    choice = input("Choose a ranking method (1-3): ").strip()

    if choice not in {"1", "2", "3"}:
        print("❌ Invalid choice.")
        return

    try:
        with conn.cursor() as cursor:
            if choice == "1":
                # Highest rated games (with fallback if unrated)
                query = """
                    SELECT v.title, r.rating
                    FROM rates r
                    JOIN videogame v ON r.videogameid = v.videogameid
                    WHERE r.username = %s
                    ORDER BY r.rating DESC
                    LIMIT 10;
                """
                cursor.execute(query, (username,))

            elif choice == "2":
                # Most played games
                query = """
                    SELECT v.title,
                           SUM(EXTRACT(EPOCH FROM (p.session_end - p.session_start)) / 60) AS total_minutes
                    FROM plays p
                    JOIN videogame v ON p.videogameid = v.videogameid
                    WHERE p.username = %s
                    GROUP BY v.title
                    ORDER BY total_minutes DESC
                    LIMIT 10;
                """
                cursor.execute(query, (username,))

            elif choice == "3":
                # Combination metric: rating × log(playtime + 1)
                query = """
                    SELECT v.title,
                           r.rating,
                           SUM(EXTRACT(EPOCH FROM (p.session_end - p.session_start)) / 60) AS total_minutes,
                           ROUND(r.rating * LOG(10, SUM(EXTRACT(EPOCH FROM (p.session_end - p.session_start)) / 60 + 1)), 2) AS score
                    FROM plays p
                    JOIN rates r ON p.videogameid = r.videogameid AND p.username = r.username
                    JOIN videogame v ON p.videogameid = v.videogameid
                    WHERE p.username = %s
                    GROUP BY v.title, r.rating
                    ORDER BY score DESC
                    LIMIT 10;
                """
                cursor.execute(query, (username,))

            results = cursor.fetchall()
            if not results:
                print("⚠️ No data found.")
                return

            print("\n🎮 Your Top 10 Games:\n")
            if choice == "1":
                for i, (title, rating) in enumerate(results, start=1):
                    print(f"{i}. {title} — ⭐ {rating}/5")
            elif choice == "2":
                for i, (title, playtime) in enumerate(results, start=1):
                    print(f"{i}. {title} — ⏱️ {playtime:.2f} minutes")
            else:
                for i, (title, rating, playtime, score) in enumerate(results, start=1):
                    print(f"{i}. {title} — ⭐ {rating}/5 | ⏱️ {playtime:.2f} min | 🥇 Score: {score}")

    except psycopg2.DatabaseError as e:
        print(f"❌ Database error: {e}")
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

