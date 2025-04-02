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