# date: 3/16/25
# author: LIV JASZCZAK

# defining important constants and data structures
# number of rows in a primary table - our project requirements said 1000s to 10000s so we'd have enough for data analysis
primary_row_count = 15000

# maximum number of connection retries - this number is arbitrarily chosen
MAX_RETRIES = 4

# number of seconds between each connection attempt - arbitrarily chosen
TRY_DELAY = 2

# ESRB rating list
ESRB_list = ["EC", "E", "E10+", "T", "M", "AO"]

#lists to help generate fake titles
#format 1 : adjective noun
# format 2: verb the noun
adjective_lst = [
    "Shadow", "Neon", "Frozen", "Dark", "Cosmic", "Turbo", "Quantum", "Rogue", "Mystic", "Lunar",
    "Infernal", "Cyber", "Enchanted", "Haunted", "Arcane", "Savage", "Radiant", "Forsaken", "Crimson", "Celestial",
    "Doomed", "Ancient", "Vengeful", "Titanic", "Ethereal", "Abyssal", "Demonic", "Glorious", "Merciless", "Primordial",
    "Tactical", "Blazing", "Stormy", "Hollow", "Mythic", "Feral", "Wicked", "Chaotic", "Futuristic", "Corrupted",
    "Draconic", "Mechanical", "Omniscient", "Unstoppable", "Wretched", "Eclipse", "Cursed", "Legendary", "Phantom", "Spectral",
    "Augmented", "Stealthy", "Dystopian", "Surreal", "Empowered", "Apocalyptic", "Divine", "Immortal", "Unholy", "Reckless",
    "Hallowed", "Fabled", "Electric", "Vortex", "Starborn", "Venomous", "Runic", "Unyielding", "Daring", "Blighted",
    "Oblivion", "Eldritch", "Shattered", "Timeless", "Dreaded", "Thunderous", "Unbreakable", "Revered", "Celestial", "Inferno",
    "Ghastly", "Overpowered", "Exiled", "Echoing", "Pestilent", "Serpentine", "Unchained", "Void", "Warped", "Brutal"
]

noun_lst = [
    "Titan", "Rift", "Horizon", "Legacy", "Dungeon", "Empire", "Champion", "Outlaw", "Sorcery", "Racer",
    "Gauntlet", "Phantom", "Fury", "Nightmare", "Arena", "Warlord", "Warrior", "Sentinel", "Overlord", "Mystic",
    "Knight", "Assassin", "Hunter", "Battalion", "Reaper", "Samurai", "Cyber", "Wizard", "Gunslinger", "Crusader",
    "Shadow", "Bounty", "Pilot", "Vanguard", "Champion", "Guardian", "Revolt", "Reckoning", "Conquest", "Doom",
    "Specter", "Striker", "Commander", "Nexus", "Avatar", "Chronicle", "Odyssey", "Expedition", "Pioneer", "Nomad",
    "Exile", "Survivor", "Outcast", "Artifact", "Relic", "Portal", "Beacon", "Catalyst", "Enigma", "Echo",
    "Inferno", "Apocalypse", "Nemesis", "Dominion", "Rebellion", "Eclipse", "Armageddon", "Annihilation", "Sanctuary", "Uprising",
    "Storm", "Requiem", "Genesis", "Retribution", "Fortress", "Revolution", "Legion", "Prophecy", "Anarchy", "Dystopia",
    "Havoc", "Cataclysm", "Vortex", "Drifter", "Sentience", "Pulse", "Manifest", "Augment", "Deception", "Paradox"
]

verb_lst = [
    "Attack", "Battle", "Build", "Capture", "Chase", "Collect", "Command", "Conquer", "Craft",
    "Defeat", "Defend", "Destroy", "Discover", "Dodge", "Dominate", "Escape", "Explore", "Fight",
    "Forge", "Gather", "Hack", "Harvest", "Hide", "Hunt", "Jump", "Level", "Loot", "Master",
    "Mine", "Navigate", "Overcome", "Pilot", "Plunder", "Protect", "Race", "Raid", "Rescue",
    "Revive", "Ride", "Shoot", "Slay", "Solve", "Spawn", "Survive", "Trade", "Train", "Traverse",
    "Upgrade", "Venture", "Wield", "Win", "Advance", "Aim", "Assemble", "Brawl", "Break", "Charge",
    "Climb", "Commandeer", "Counter", "Crush", "Customize", "Dash", "Decipher", "Duel", "Evade",
    "Execute", "Expand", "Hack", "Harvest", "Inflict", "Intercept", "Investigate", "Launch", "Lurk",
    "Maneuver", "Manipulate", "Mobilize", "Obliterate", "Operate", "Patrol", "Persist", "Pillage",
    "Plunge", "Rebuild", "Reclaim", "Refine", "Regroup", "Repel", "Research", "Sabotage", "Scout",
    "Seize", "Sneak", "Sprint", "Storm", "Tame", "Vanquish"
]

# importing libraries
from faker import Faker  # This library that generates fake data
import time # so we can delay reconnect attempts
import psycopg2  # for connecting python and postgre
import random
from psycopg2 import extras
from db import get_db_connection  # Ensure db.py is in the same directory/folder

# create a faker object and access Faker methods
fake = Faker()

# Generates random data for the GAMES table
def make_games_data():
    title_determiner = random.random()

    if title_determiner > 0.5:
        adj = random.choice(adjective_lst)
        noun = random.choice(noun_lst)
        title = adj+" "+noun
    else:
        noun = random.choice(noun_lst)
        verb = random.choice(verb_lst)
        title = verb+" the "+noun


    rating = random.choice(ESRB_list)

    return title, rating


# Generate PRIMARY_ROW_COUNT rows of data
def make_games_rows(primary_row_count, games_data):
    for i in range(primary_row_count):
        games_data.append(make_games_data())

# to make an attempt to reconnect the database
# originally written by KIFEKACHUKWU NWOSU in collection.py
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn

# Function to insert the created user data onto the server
def insert_games_data(games_data, MAX_RETRIES):
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
                INSERT INTO VIDEOGAME (title, ESRB_Rating)  
                VALUES %s
                """
                # a bulk insert for the more efficient insertion of 15000 rows
                extras.execute_values(cursor, insert_query, games_data)

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
    games_data = []

    make_games_rows(primary_row_count, games_data)
    insert_games_data(games_data, MAX_RETRIES)
    print("Hi there.")

main()

