import datetime

from db import get_db_connection # Ensure db.py is in the same directory
# AUTHOR : Christabel Osei
# Author : Kiffy Nwosu
conn = get_db_connection()
def play_video_game(cls):
    """Logs when a user starts and ends playing a video game."""
    game_name = input("Enter the name of the video game you want to play: ").strip()
    with cls.conn.cursor() as cursor:
        cursor.execute('SELECT "video_game_id" FROM "video_games" WHERE name = %s', (game_name,))
        result = cursor.fetchone()
        if not result:
            print("Game not found.")
            return
        game_id = result[0]
        start_time = datetime.datetime.now()
        print(f"🎮 You started playing {game_name} at {start_time}.")
        input("Press Enter to stop playing...")
        end_time = datetime.datetime.now()
        play_time = (end_time - start_time).total_seconds() // 60  # Convert seconds to minutes
        cursor.execute("""
            INSERT INTO game_play_sessions (user_id, video_game_id, start_time, end_time, play_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (cls.user_id, game_id, start_time, end_time, play_time))
        cls.conn.commit()
        print(f" You played {game_name} for {play_time} minutes.")

def videogame_search_menu():
    print("What would you like to search by?")
    print("1: VideoGame Name")
    print("2: VideoGame Release Date")
    print("3: Platform")
    print("4: Genre")
    print("5: Price")
    print("6: Developers")

    def search_video_games_by_name():
        if conn is None:
            print("Failed to connect to the database.")
            return

        name =input("Please enter the name of the Video Game you would like to search for").strip()
        print(f"Searching for {name} by name, sorted alphabetically by name and release date")

        query = """
            SELECT name,
                   platform,
                   releasedate,
                   developer,
                   publisher,
                   play_time,
                   esrb_rating,
                   genre,
                   price
            FROM videogames
            WHERE name ILIKE %s
            ORDER BY name ASC, releasedate ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(query, (f"%{name}%",))
            result_set = cursor.fetchall()

        print_result(result_set)

    def print_result(result_set):
        for row in result_set:
            print(row)

    @classmethod
    def rate_video_game(cls):
        """Allows users to rate a video game with a star rating (1-5)."""
        game_name = input("Enter the name of the video game you want to rate: ").strip()
        with cls.conn.cursor() as cursor:
            cursor.execute('SELECT "video_game_id" FROM "video_games" WHERE name = %s', (game_name,))
            result = cursor.fetchone()
            if not result:
                print("Game not found.")
                return
            game_id = result[0]
            while True:
                try:
                    rating = int(input("Enter your star rating (1-5): ").strip())
                    if 1 <= rating <= 5:
                        break
                    else:
                        print(" Please enter a number between 1 and 5.")
                except ValueError:
                    print(" Invalid input. Please enter a number between 1 and 5.")
            cursor.execute("""
                INSERT INTO game_ratings (user_id, video_game_id, rating, rated_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id, video_game_id) DO UPDATE
                SET rating = EXCLUDED.rating, rated_at = EXCLUDED.rated_at
            """, (cls.user_id, game_id, rating))
            cls.conn.commit()
            print(f"✅ You rated {game_name} with {rating} stars.")

    @classmethod
    def play_random_game(cls):
        """Allows the user to play a random game from their collection and logs play time."""
        with cls.conn.cursor() as cursor:
            cursor.execute('''
                SELECT vg.name, vg.video_game_id FROM video_games vg
                JOIN user_collections uc ON vg.video_game_id = uc.video_game_id
                WHERE uc.user_id = %s
                ORDER BY RANDOM() LIMIT 1
            ''', (cls.user_id,))
            result = cursor.fetchone()
            if not result:
                print("⚠️ You have no games in your collection to play.")
                return
            game_name, game_id = result
            start_time = datetime.datetime.now()
            print(f"🎮 You started playing {game_name} at {start_time}.")
            input("Press Enter to stop playing...")
            end_time = datetime.datetime.now()
            play_time = (end_time - start_time).total_seconds() // 60  # Convert seconds to minutes
            cursor.execute("""
                INSERT INTO game_play_sessions (user_id, video_game_id, start_time, end_time, play_time)
                VALUES (%s, %s, %s, %s, %s)
            """, (cls.user_id, game_id, start_time, end_time, play_time))
            cls.conn.commit()
        print(f"✅ You played {game_name} for {play_time} minutes.")

# Function to reconnect to the database
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
