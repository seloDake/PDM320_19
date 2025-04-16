import datetime
import re
import psycopg2
import random
from db import get_db_connection # Ensure db.py is in the same directory

# AUTHOR : Christabel Osei
conn = get_db_connection()

class User:
    # user_id = -1  # Static user ID
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
                cls.user_id = result[0]
                cls.login_checker = True
                current_time = datetime.datetime.now()

                cursor.execute("""UPDATE login_record SET login_date = %s WHERE username = %s""", (current_time, cls.user_id))
                if cursor.rowcount == 0:
                    cursor.execute("""INSERT INTO login_record (username, login_date)VALUES (%s, %s)""", (cls.user_id, current_time))
                cls.conn.commit()
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
        
        while True:
            last_name = input("Please enter last name: ").strip()
            if not re.match("^[A-Za-z]+$", last_name):
                print("Error: Last name must contain only letters (no spaces, numbers, or special characters).")
            elif len(last_name) <= 1:
                print("Error: Last name must be at least 2 characters long.")
            else:
                break
        
        
        while True:
            email = input("Please enter your email: ").strip()
            if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
                print("Error: Invalid email format. Please enter a valid email (e.g., user@example.com).")
            with cls.conn.cursor() as cursor:
                cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    print("Error: Email is already registered. Please use a different email.")
                    continue
            break
       

        while True:
            username = input("Please enter a new username: ").strip()
            if cls.is_username_taken(username) != -1:
                print("Username already taken - please enter a different one.")
            else:
                break

        while True:
            password = input("Please enter a new password: ").strip()
            if len(password) < 8:
                print("Password must be at least 6 characters long.")
                continue
            if not re.search(r"[A-Z]", password):
                print("Error: Password must contain at least one uppercase letter (A-Z).")
                continue
            if not re.search(r"[a-z]", password):
                print("Error: Password must contain at least one uppercase letter (A-Z).")
                continue
            if not re.search(r"[@$!%?&]", password):
                print("Error: Password must contain at least one uppercase letter (A-Z).")
                continue
            break

        current_time = datetime.datetime.now()
        selected_platform_id = cls.assign_platform()

        try:
            with cls.conn.cursor() as cursor:
                # increment_user_id = cls.increment_counter_user_id()
               

                cursor.execute("""
                    INSERT INTO users (username, email,first_name,last_name,password,creation_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (username, email, first_name,last_name,password,current_time))
                cursor.execute("""INSERT INTO login_record (username, login_date)VALUES (%s, %s)""", (username, current_time))
                cursor.execute("""INSERT INTO owns (username, platformid)VALUES (%s, %s)""", (username, selected_platform_id))
                cls.conn.commit()
                print("Your account has been created! Please sign in to access other functionalities.")
                print("You login_record has been updated")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            cls.conn.rollback()

    @staticmethod
    def assign_platform():
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT platformid, name FROM platform ORDER BY RANDOM() LIMIT 10")
            platforms = cursor.fetchall()

        print("\n🎮 Select a platform from the list below:")
        for idx, (platformid, name) in enumerate(platforms, 1):
            print(f"{idx}: {name}")

        while True:
            try:
                choice = int(input("Enter the number of your chosen platform: ").strip())
                if 1 <= choice <= len(platforms):
                    return platforms[choice - 1][0]
                else:
                    print("Invalid choice. Try a number from the list.")
            except ValueError:
                print("Please enter a valid number.")

    @classmethod
    def manage_platforms(cls):
        """Allows a user to view and add platforms."""
        while True:
            print("\n🎮 Platform Management Menu")
            print("1: View my platforms")
            print("2: Add a new platform")
            print("3: Back to main menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                cls.view_user_platforms()
            elif choice == "2":
                cls.add_new_platform()
            elif choice == "3":
                break
            else:
                print("Invalid input. Try again.")

    @classmethod
    def view_user_platforms(cls):
        with cls.conn.cursor() as cursor:
            cursor.execute("""SELECT p.name FROM owns o JOIN platform p ON o.platformid = p.platformid WHERE o.username = %s""", (cls.user_id,))
            platforms = cursor.fetchall()

            if not platforms:
                print("⚠️ You don't have any platforms yet.")
            else:
                print("\n🕹️ Your Platforms:")
                for p in platforms:
                    print(f"– {p[0]}")

    @classmethod
    def add_new_platform(cls):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Get 10 random platforms
            cursor.execute("SELECT platformid, name FROM platform ORDER BY RANDOM() LIMIT 10")
            platforms = cursor.fetchall()

            print("\n🎮 Choose a platform to add:")
            for idx, (pid, name) in enumerate(platforms, 1):
                print(f"{idx}: {name}")

            while True:
                try:
                    choice = int(input("Enter the number of your chosen platform: ").strip())
                    if 1 <= choice <= len(platforms):
                        selected_platform_id = platforms[choice - 1][0]

                        # Check if already owned
                        cursor.execute("""SELECT 1 FROM owns WHERE username = %s AND platformid = %s""", (cls.user_id, selected_platform_id))
                        if cursor.fetchone():
                            print("⚠️ You already own this platform.")
                            return

                        # Add new platform
                        cursor.execute("""INSERT INTO owns (username, platformid) VALUES (%s, %s)""", (cls.user_id, selected_platform_id))
                        cls.conn.commit()
                        print("✅ Platform added successfully!")
                        return
                    else:
                        print("Invalid selection. Try again.")
                except ValueError:
                    print("Please enter a number.")

    
    @staticmethod
    def print_begin_menu():
        print("\nWelcome to the  Video Game!")
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
            print("3: Play Video Games")
            print("4: Rate Video Games")
            print("5: Follow and unfollow a user")
            print("6: Search for a video game: ")
            print("7: Manage Platforms")
            print("8: View Top 20 Games")
            print("9: View Top releases of the month")
            print("10: Most Played Video Games amongst followers")
            print("11: Logout")
            choice = input("Enter your choice: ")
            if choice == "2":
                print("Accessing collections...")
                from collection import printCollectionsMenu
                printCollectionsMenu(cls.user_id)
            elif choice == "3":
                print("Play Video Game")
                from videoGame import printVideoGamesMenu
                printVideoGamesMenu(cls.user_id)
            elif choice == "4":
                print("Rating videoGames...")
                from videoGame import rate_video_game
                rate_video_game(cls.user_id, conn)
            elif choice == "5":
                print("Following users...")
                cls.follow_unfollow_menu()
            elif choice == "6":
                from videoGame import printVideoGamesMenu
                printVideoGamesMenu(cls.user_id)
            elif choice == "7":
                cls.manage_platforms()
            elif choice == "8":
                from Recommendation import top_20_popular_last_90_days
                top_20_popular_last_90_days(cls.user_id)
            elif choice == "9":
                from Recommendation import top_releases_of_this_month
                top_releases_of_this_month(cls.user_id)
            elif choice == "10":
                from Recommendation import  amongstFollowers
                amongstFollowers(cls.user_id)
            elif choice == "11":
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
            print("Username:", follow_id)
            print("Username:", cls.user_id)
            cursor.execute("INSERT INTO follow_unfollow (followerusername, followeeusername) VALUES (%s, %s)",
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
            cursor.execute("DELETE FROM follow_unfollow WHERE followerusername = %s AND followeeusername = %s",
                           (cls.user_id, unfollow_id))
            cls.conn.commit()
            print(" Successfully unfollowed the user!")
    
   
# Function to reconnect to the database
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn