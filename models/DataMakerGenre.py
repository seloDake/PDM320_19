# date: 3/16/25
# author: LIV JASZCZAK

# defining important constants and data structures

# maximum number of connection retries - this number is arbitrarily chosen
MAX_RETRIES = 4

# number of seconds between each connection attempt - arbitrarily chosen
TRY_DELAY = 2

# importing libraries
from faker import Faker  # This library that generates fake data
import time # so we can delay reconnect attempts
import psycopg2  # for connecting python and postgre
import random
from psycopg2 import extras
from db import get_db_connection  # Ensure db.py is in the same directory/folder

# a list of a bunch of video game genres I found by asking ChatGPT to compile
# genres and subgenres from these links:
# https://tvtropes.org/pmwiki/pmwiki.php/Main/VideoGameGenres
# https://www.mobygames.com/genre/
# https://en.wikipedia.org/wiki/List_of_video_game_genres
genre_lst = ["Action", "Platformer", "Shooter", "First-person shooter (FPS)",
    "Third-person shooter (TPS)", "Fighting", "Beat 'em up / Brawler",
    "Stealth", "Survival", "Rhythm", "Battle Royale", "Action-Adventure",
    "Survival Horror", "Metroidvania", "Adventure", "Text Adventure",
    "Graphic Adventure", "Visual Novel", "Interactive Movie",
    "Real-time 3D Adventure", "Puzzle", "Breakout Clone", "Logical",
    "Physics Game", "Programming Game", "Puzzle-Platformer",
    "Trial-and-Error / Exploration", "Hidden Object", "Reveal the Picture",
    "Tile-Matching", "Traditional Puzzle", "Role-Playing Game (RPG)",
    "Action RPG", "Computer RPG (CRPG)",
    "Massively Multiplayer Online RPG (MMORPG)", "Roguelike", "Tactical RPG",
    "Sandbox RPG", "First-Person Party-Based RPG", "Monster Tamer",
    "Simulation", "Construction and Management Simulation", "Life Simulation",
    "Vehicle Simulation", "Strategy", "4X Game", "Artillery Game",
    "Auto Battler (Auto Chess)", "Multiplayer Online Battle Arena (MOBA)",
    "Real-Time Strategy (RTS)", "Real-Time Tactics (RTT)", "Tower Defense",
    "Turn-Based Strategy (TBS)", "Turn-Based Tactics (TBT)",
    "Wargame", "Grand Strategy Wargame", "Sports", "Racing", "Sports Game",
    "Competitive", "Sports-Based Fighting", "Massively Multiplayer Online (MMO)",
    "Board Game or Card Game", "Parental Sim", "Casino Game",
    "Digital Collectible Card Game", "Digital Therapeutic Video Game",
    "Gacha Game", "Horror Game", "Idle Game", "Party Game", "Photography Game",
    "Social Deduction Game", "Trivia Game", "Typing Game", "Advergame",
    "Art Game", "Casual Game", "Christian Game", "Educational Game", "Esports"
    "Exergame (Fitness Game)", "Personalized Game", "Serious Game",
    "Live Interactive Game", "Sandbox", "Creative", "Open World","First-Person",
    "Third-Person (Other)", "Audio Game", "Behind View", "Diagonal-Down",
    "Side View", "Text-Based / Spreadsheet", "Top-Down", "2D Scrolling",
    "Cinematic Camera", "Fixed / Flip-Screen", "Free Camera", "Isometric",
    "Anime / Manga", "Augmented Reality", "Full Motion Video (FMV)",
    "Live Action", "Video Backdrop", "Meditative / Zen", "Persistent",
    "Real-Time", "Turn-Based", "4X", "Arcade", "Artillery", "Board Game",
    "Cards / Tiles", "Chess", "City Building / Construction Simulation",
    "Dating Simulation", "Falling Block Puzzle", "Gambling Elements",
    "Game Show / Trivia / Quiz", "Graphic Adventure", "Hack and Slash",
    "Hidden Object", "Hunting", "Interactive Book",
    "Interactive Fiction / Text Adventure", "Japanese-Style RPG (JRPG)",
    "Japanese-Style Adventure", "Life / Social Simulation",
    "Managerial / Business Simulation", "Massively Multiplayer",
    "Mental Training", "Metroidvania",
    "Mini-Games", "Music / Rhythm", "Paddle / Pong", "Party Game",
    "Pinball", "Platform", "Puzzle Elements", "Quick Time Events (QTEs)",
    "RPG Elements", "Rail Shooter", "Real-Time Strategy (RTS)",
    "Real-Time Tactics (RTT)", "Roguelike", "Sandbox / Open World",
    "Shooter", "Stealth", "Sports Themes", "Educational Categories",
    "Vehicular Themes", "Settings", "Narrative Themes/Topics", "Add-on",
    "Special Edition", "Other Attributes"
]

# create a faker object and access Faker methods
fake = Faker()

# to make an attempt to reconnect the database
# originally written by KIFEKACHUKWU NWOSU in collection.py
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn

# Function to insert the created user data onto the server
def insert_genre_data(users_data, MAX_RETRIES):
    # a while loop and counter so we don't keep trying to connect to the database over and over again
    attempts = 0

    while attempts < MAX_RETRIES:
        connection = get_db_connection()
        if connection is None:
            print("Couldn't't connect to the database.")
            return

        try:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO GENRE (genrename) 
                VALUES (%s)
                """
                # Individually insert each item in the list of genre names
                for item in genre_lst:
                    item_list = (item)
                    cursor.execute(insert_query, (item_list,))

                connection.commit()
                print(f"Data Committed")
                return  # Exit on success

        # in the case of a failure to connect...
        except psycopg2.OperationalError as e:
            # print a message so the user can see what's going wrong and how many attempts are left
            print(f"Operational error: {e}. Retrying ({attempts + 1}/{MAX_RETRIES})...")
            if connection:
                connection.close()
            time.sleep(TRY_DELAY)
            attempts += 1

        # announce any database errors and rollback any database edits to prevent half-way changes
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            connection.rollback()
            return  # Exit on failure
        finally:
            if connection:
                connection.close()

    #let the user know if we ran out of tries to connect to the database
    print("Max retries reached. Could not create collection.")

# executes the process of adding user data by calling above functions
def main():
    genre_data = []

    insert_genre_data(genre_data, MAX_RETRIES)
    print("Hi there.")

main()

