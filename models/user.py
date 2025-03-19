import datetime
import psycopg2
import random
from db import get_db_connection # Ensure db.py is in the same directory
# AUTHOR : Christabel Osei
conn = get_db_connection()

class User:
    user_id = -1  # Static user ID
    login_checker = False
    conn = None
    session = None

    def __init__(self):
        self.conn = get_db_connection()
        
    @classmethod
    def is_username_taken(cls,username):
        """Checks if a username already exists in the database."""
        with cls.conn.cursor() as cursor:
            cursor.execute('SELECT "username" FROM "users" WHERE username = %s', (username,))
            result = cursor.fetchone()
            return result[0] if result else -1
        
    @classmethod
    def login(cls):
        """Logs in a user, stores the userID, and updates the last accessed timestamp."""
        if cls.conn is None or cls.conn.closed != 0:
            print("Database connection lost. Reconnecting...")
            cls.conn = get_db_connection()
            if cls.conn is None:
                print("Could not establish a database connection.")
                return
        print("\nWelcome to login. Please enter credentials below:")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        with cls.conn.cursor() as cursor:
            cursor.execute('SELECT "username" FROM "users" WHERE username = %s AND password = %s', (username, password))
            result = cursor.fetchone()

            if result:
                # cls.user_id = result[0]
                # cls.login_checker = True
                # current_time = datetime.datetime.now()

                # cursor.execute('UPDATE "users" SET "accessid" = %s WHERE "username" = %s', (current_time, cls.user_id))
                # cls.conn.commit()

                print("Login successful!")
                cls.print_main_menu()
            else:
                print("Could not login - try again or create an account.")
                cls.print_begin_menu()

    @classmethod
    def logout(cls):
        """Logs out the user by resetting the userID and login checker."""
        cls.user_id = -1
        cls.login_checker = False
        print("You are now logged out and disconnected, goodbye 😉")
        
        
    @classmethod
    def increment_counter_user_id(cls):
        """Finds the next available user ID by getting the max userID and adding 1."""
        with cls.conn.cursor() as cursor:
            cursor.execute('SELECT MAX("username") FROM "users"')
            result = cursor.fetchone()
            return (result[0] or 0) + 1
                
    @classmethod
    def create_account(cls):
        """Creates a new user"""
        cls.conn = get_db_connection()
        print("Welcome to Account Creation. Please enter your crendentials below")
        

        first_name = input("Please enter first name: ").strip()
        last_name = input("Please enter last name: ").strip()
        email = input("Please enter your email: ").strip()
       

        while True:
            username = input("Please enter a new username: ").strip()
            if cls.is_username_taken(username) != -1:
                print("Username already taken - please enter a different one.")
            else:
                break

        while True:
            password = input("Please enter a new password: ").strip()
            if len(password) < 6:
                print("Password must be at least 6 characters long.")
            else:
                break

        current_time = datetime.datetime.now()

        try:
            with cls.conn.cursor() as cursor:
                # increment_user_id = cls.increment_counter_user_id()
                cursor.execute("""
                    INSERT INTO users (username, email, password, first_name, last_name,creation_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (username, email, first_name, last_name,password,current_time))
                cls.conn.commit()
                print("Your account has been created! Please sign in to access other functionalities.")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            cls.conn.rollback()


    
    @staticmethod
    def print_begin_menu():
        print("\nWelcome to the Video Game!")
        print("Please sign in or create account with the folloeing commands: ")
        print("1: Create Account")
        print("0: Login")
        print("9: Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            User.create_account()
        elif choice == "0":
            User.login()
        elif choice == "9":
            print("Exiting application.")
            exit()
        else:
            print("Invalid option. Try again.")
            User.print_begin_menu()



    @classmethod
    def print_main_menu(cls):
        """Displays the main menu and directs the user based on their choice."""
        while True:
            print("\nFind below more functionality:")
            print("2: Access and Edit Collections")
            print("3: Search for Video Games")
            print("4: Rate Video Games")
            print("5: Follow other Users")
            print("9: Logout")
            choice = input("Enter your choice: ")
            if choice == "2":
                print("Accessing collections...")
                
            elif choice == "3":
                print("Searching for videogames...")
                cls.search_video_game()
                
            
            elif choice == "4":
                print("Rating movies...")
                cls.rate_video_game()
            elif choice == "5":
                print("Following users...")
                cls.follow_unfollow_menu()
            elif choice == "9":
                cls.logout()
                break
            else:
                print("Invalid choice, please try again.")

    @classmethod
    def follow_unfollow_menu(cls):
        """Displays the Follow/Unfollow Menu"""
        while True:
            print("\nWelcome to the Followers Menu!")
            print("Here are the available commands:")
            print("0: Reprint the followers menu")
            print("1: Follow A User")
            print("2: Unfollow A User")
            print("3: Return to the main menu\n")
            command = input("Enter the number that corresponds to the command you wish to execute: ")
            if command == "0":
                continue
            elif command == "1":
                cls.follow_user()
            elif command == "2":
                cls.unfollow_user()
            elif command == "3":
                break
            else:
                print("⚠️ Please pick a valid number")

    @classmethod
    def follow_user(cls):
        """Allows a user to follow another user by Name or Email."""
        print("You have selected to follow a user.")
        print("1: Follow a user by Name")
        print("2: Follow a user by Email")
        choice = input("Enter your choice: ")

        with cls.conn.cursor() as cursor:
            if choice == "1":
                first_name = input("Enter the first name of the person you would like to follow: ").strip()
                last_name = input("Enter the last name of the person you would like to follow: ").strip()
                cursor.execute('SELECT "username" FROM "users" WHERE first_name = %s AND last_name = %s', (first_name, last_name))
                result = cursor.fetchone()
            elif choice == "2":
                email = input("Enter the email address of the user you would like to follow: ").strip()
                cursor.execute('SELECT "username" FROM "users" WHERE email = %s', (email,))
                result = cursor.fetchone()
            else:
                print(" Invalid option.")
                return

            if not result:
                print(" User not found.")
                return

            follow_id = result[0]
            cursor.execute("INSERT INTO user_followers (follower_id, following_id) VALUES (%s, %s)",
                           (cls.user_id, follow_id))
            cls.conn.commit()
            print(" Successfully followed the user!")

    @classmethod
    def unfollow_user(cls):
        """Allows a user to unfollow another user by Name or Email."""
        print("You have selected to unfollow a user.")
        print("1: Unfollow a user by Name")
        print("2: Unfollow a user by Email")
        choice = input("Enter your choice: ")

        with cls.conn.cursor() as cursor:
            if choice == "1":
                first_name = input("Enter the first name of the person you would like to unfollow: ").strip()
                last_name = input("Enter the last name of the person you would like to unfollow: ").strip()
                cursor.execute('SELECT "username" FROM "users" WHERE first_name = %s AND last_name = %s', (first_name, last_name))
                result = cursor.fetchone()
            elif choice == "2":
                email = input("Enter the email address of the user you would like to unfollow: ").strip()
                cursor.execute('SELECT "username" FROM "users" WHERE email = %s', (email,))
                result = cursor.fetchone()
            else:
                print("Invalid option.")
                return

            if not result:
                print(" User not found.")
                return

            unfollow_id = result[0]
            cursor.execute("DELETE FROM user_followers WHERE follower_id = %s AND following_id = %s",
                           (cls.user_id, unfollow_id))
            cls.conn.commit()
            print(" Successfully unfollowed the user!")

    @classmethod
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

    @classmethod
    def search_video_game(cls):
        """Searches for video games based on user criteria."""
        print("\nSearch for Video Games")
        search_term = input("Enter game name, platform, release date (YYYY-MM-DD), developer, price, or genre: ").strip()
        sort_by = input("Sort by (name, price, genre, release_year, developer) [asc/desc]: ").strip()
        order = "ASC" if "asc" in sort_by.lower() else "DESC"
        sort_column = "name"  # Default sorting by name

        if "price" in sort_by.lower():
            sort_column = "price"
        elif "genre" in sort_by.lower():
            sort_column = "genre"
        elif "release_year" in sort_by.lower():
            sort_column = "release_date"
        elif "developer" in sort_by.lower():
            sort_column = "developer"

        with cls.conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT name, platform, release_date, developer, publisher, play_time, age_rating, user_rating, genre
                FROM video_games
                WHERE LOWER(name) LIKE %s OR LOWER(platform) LIKE %s OR release_date::TEXT LIKE %s 
                      OR LOWER(developer) LIKE %s OR CAST(price AS TEXT) LIKE %s OR LOWER(genre) LIKE %s
                ORDER BY {sort_column} {order}
            """, (f"%{search_term.lower()}%", f"%{search_term.lower()}%", f"%{search_term}%',"
                  f"%{search_term.lower()}%", f"%{search_term}%", f"%{search_term.lower()}%"))
            results = cursor.fetchall()
            if not results:
                print("⚠️ No games found matching your search.")
                return
            print("\nSearch Results:")
            for game in results:
                print(f"{game[0]} | {game[1]} | {game[2]} | {game[3]} | {game[4]} | {game[5]} min | Age: {game[6]} | User Rating: {game[7]} | Genre: {game[8]}")


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
    return conn