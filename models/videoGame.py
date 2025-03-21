import datetime
import psycopg2
from db import get_db_connection # Ensure db.py is in the same directory
from datetime import date

# AUTHOR : Christabel Osei
# Author : Kiffy Nwosu
conn = get_db_connection()

def videogame_search_menu():
    print("What would you like to search by?")
    print("1: VideoGame Name")
    print("2: VideoGame Release Date")
    print("3: Platform")
    print("4: Genre")
    print("5: Price")
    searchby = input("what would you like to search by? ")
    if searchby == "1":
        search_video_games_by_name()
    elif searchby == "2":
        search_video_games_by_release_date(conn)


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
        print("   1. Name & Release Date (Ascending) [Default]")
        print("   2. Name & Release Date (Descending)")
        print("   3. Price (Ascending)")
        print("   4. Price (Descending)")
        print("   5. Genre (Ascending)")
        print("   6. Genre (Descending)")
        print("   7. Release Year (Ascending)")
        print("   8. Release Year (Descending)")

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

        print("\n📌 Sort results by:")
        print("1️⃣ Video Game Name (Ascending)")
        print("2️⃣ Video Game Name (Descending)")
        print("3️⃣ Price (Lowest to Highest)")
        print("4️⃣ Price (Highest to Lowest)")
        print("5️⃣ Release Year (Oldest to Newest)")
        print("6️⃣ Release Year (Newest to Oldest)")
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


def search_video_games_by_release_date(conn):
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()

        print("Do you want to search by:\n1: Month\n2: Year\n3: Exact Date")
        search_option = input("Choose an option (1/2/3): ").strip()

        query = ""
        query_param = None

        if search_option == "1":  # Search by Month
            month = int(input("Enter the month as a number (i.e., for October enter 10): ").strip())
            query = """
                SELECT v.title,
                       v.esrb_rating,
                       h.release_date,
                       h.price,
                       p.name,
                       COALESCE(array_agg(DISTINCT g.genrename), '{}') AS genres
                FROM videogame v
                JOIN hosts h ON v.videogameid = h.videogameid
                JOIN platform p ON h.platformid = p.platformid
                JOIN game_is_genre gg ON v.videogameid = gg.videogameid
                JOIN genre g ON gg.genreid = g.genreid
                WHERE EXTRACT(MONTH FROM h.release_date) = %s
                GROUP BY v.videogameid, h.release_date, h.price, p.name
                ORDER BY v.title, h.release_date;
            """
            query_param = (month,)

        elif search_option == "2":
            year = int(input("Enter the year: ").strip())
            query = """
                SELECT v.title,
                       v.esrb_rating,
                       h.release_date,
                       h.price,
                       p.name,
                       COALESCE(array_agg(DISTINCT g.genrename), '{}') AS genres
                FROM videogame v
                JOIN hosts h ON v.videogameid = h.videogameid
                JOIN platform p ON h.platformid = p.platformid
                JOIN game_is_genre gg ON v.videogameid = gg.videogameid
                JOIN genre g ON gg.genreid = g.genreid
                WHERE EXTRACT(YEAR FROM h.release_date) = %s
                GROUP BY v.videogameid, h.release_date, h.price, p.name
                ORDER BY v.title, h.release_date;
            """
            query_param = (year,)

        elif search_option == "3":
            year = int(input("Enter the year: ").strip())
            month = int(input("Enter the month: ").strip())
            day = int(input("Enter the day: ").strip())
            release_date = date(year, month, day)

            query = """
                SELECT v.title,
                       v.esrb_rating,
                       h.release_date,
                       h.price,
                       p.name,
                       COALESCE(array_agg(DISTINCT g.genrename), '{}') AS genres
                FROM videogame v
                JOIN hosts h ON v.videogameid = h.videogameid
                JOIN platform p ON h.platformid = p.platformid
                JOIN game_is_genre gg ON v.videogameid = gg.videogameid
                JOIN genre g ON gg.genreid = g.genreid
                WHERE h.release_date = %s
                GROUP BY v.videogameid, h.release_date, h.price, p.name
                ORDER BY v.title, h.release_date;
            """
            query_param = (release_date,)

        else:
            print("❌ Not a valid option. Please choose 1, 2, or 3.")
            return

        cursor.execute(query, query_param)
        result_set = cursor.fetchall()

        if not result_set:
            print("❌ No video games found for the selected date.")
            return

        print("\n🎮 Video Games Released on Selected Date:")
        for row in result_set:
            title, esrb_rating, release_date, price, name, genres = row
            genres = genres or []  # Ensure it's always a list
            print(f"   📌 {title} | ESRB: {esrb_rating} | Released: {release_date} | Price: ${price:.2f}")
            print(f"      🎮 Platform: {name}")
            print(f"      🎭 Genres: {', '.join(genres) if genres else 'N/A'}")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

def print_result(result_set):
    for row in result_set:
        print(row)



def search_video_games_by_genre():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        genre_name = input("Please enter the genre you would like to search for: ").strip()
        if not genre_name:
            print("Invalid input. Please enter a valid genre name.")
            return

        print(f"🔍 Searching for games in the '{genre_name}' genre, sorted alphabetically...\n")

        query = """
            SELECT v.title,
                   v.esrb_rating,
                   h.release_date,
                   h.price,
                   p.name,
                   COALESCE(array_agg(DISTINCT g.genrename), '{}') AS genres
            FROM videogame v
            JOIN hosts h ON v.videogameid = h.videogameid
            JOIN platform p ON h.platformid = p.platformid
            JOIN game_is_genre gg ON v.videogameid = gg.videogameid
            JOIN genre g ON gg.genreid = g.genreid
            WHERE g.genrename ILIKE %s
            GROUP BY v.videogameid, h.release_date, h.price, p.name
            ORDER BY v.title, h.release_date;
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

        print("\n📌 Sort results by:")
        print("1️⃣ Video Game Name (Ascending)")
        print("2️⃣ Video Game Name (Descending)")
        print("3️⃣ Price (Lowest to Highest)")
        print("4️⃣ Price (Highest to Lowest)")
        print("5️⃣ Release Year (Oldest to Newest)")
        print("6️⃣ Release Year (Newest to Oldest)")
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

        print("\n📌 Sort results by:")
        print("1️⃣ Video Game Name (Ascending)")
        print("2️⃣ Video Game Name (Descending)")
        print("3️⃣ Price (Lowest to Highest)")
        print("4️⃣ Price (Highest to Lowest)")
        print("5️⃣ Release Year (Oldest to Newest)")
        print("6️⃣ Release Year (Newest to Oldest)")
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

def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")

search_video_games_by_price()