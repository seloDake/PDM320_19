import psycopg2

from db import get_db_connection
import collection
from user import User
import  videoGame
userinput = ""
conn = get_db_connection()

def amongstFollowers(user_id):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        query = """
            SELECT v.title 
            FROM videogame AS v
            JOIN plays AS p ON v.videogameid = p.videogameid
            JOIN follow_unfollow AS f ON p.username = f.followeeusername
            WHERE f.followerusername = %s
            GROUP BY v.title
            ORDER BY COUNT(v.title) DESC
            LIMIT 20;
        """



        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            result_set = cursor.fetchall()

        if not result_set:
            print("❌ No Videogames found among followers.")
            return

        print("\n🎥 Most Played VideoGa,es Among Followers:")
        for row in result_set:
            print(f"   🎬 {row[0]}")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
# a lot of them will say no u=common games due to how the dataset is computed, hwowever these ones have some but not up to 20
#ocarr
#wcameron
#piercetravis
#margaretdonovan
amongstFollowers("margaretdonovan");

def top_releases_of_this_month(user_id):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        # Ask for month and year
        month = int(input("Enter the month as a number (e.g., October = 10): ").strip())
        year = int(input("Enter the year: ").strip())

        query = """
            SELECT v.title, h.release_date, h.price, 
                   COALESCE(STRING_AGG(DISTINCT g.genrename, ', '), 'Unknown') AS genres
            FROM videogame AS v
            JOIN hosts AS h ON v.videogameid = h.videogameid
            JOIN game_is_genre AS gg ON v.videogameid = gg.videogameid
            JOIN genre AS g ON gg.genreid = g.genreid
            WHERE EXTRACT(MONTH FROM h.release_date) = %s
              AND EXTRACT(YEAR FROM h.release_date) = %s
            GROUP BY v.title, h.release_date, h.price
            ORDER BY h.release_date DESC, h.price DESC
            LIMIT 10;
        """

        with conn.cursor() as cursor:
            cursor.execute(query, (month, year))
            result_set = cursor.fetchall()

        if not result_set:
            print("❌ No top releases found for the given month and year.")
            return

        print(f"\n🎮 Top Releases for {month}/{year}:")
        for row in result_set:
            title, release_date, price, genres = row
            print(f"📌 {title} | Released: {release_date} | Price: ${price:.2f} | Genres: {genres}")

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()
    except ValueError:
        print("❌ Invalid input. Please enter a valid month (1-12) and year (e.g., 2024).")
    finally:
        if conn:
            conn.close()
top_releases_of_this_month("margaretdonovan");
