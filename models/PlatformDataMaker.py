# date: 3/17/25
# author: LIV JASZCZAK

# defining important constants and data structures

# number of rows in a primary table - our project requirements said 1000s to
# 10000s so we'd have enough for data analysis
primary_row_count = 15000

# maximum number of connection retries - this number is arbitrarily chosen
MAX_RETRIES = 4

# number of seconds between each connection attempt - arbitrarily chosen
TRY_DELAY = 2

# A list of 200 prefixes to use when making platform names. I got this list from ChatGPT
prefix_lst = [
    "Neo", "Ultra", "Cyber", "Mega", "Hyper", "Galaxy", "Star", "Power", "Vortex", "Nova",
    "Fusion", "Quantum", "Next", "Xeno", "Arc", "Turbo", "Eclipse", "Vibe", "Pixel", "Omega",
    "Infinity", "Prime", "Vision", "Zenith", "Ion", "Alpha", "Beta", "Gamma", "Cosmo", "Stream",
    "Super", "Mega", "Max", "Cloud", "Nexus", "Phantom", "Genesis", "Nova", "Hyperion", "Phantom",
    "Orbit", "Vanguard", "Impulse", "Velocity", "Vector", "Fusion", "Core", "Element", "Reactor",
    "Catalyst", "Shift", "Dynasty", "Matrix", "Redline", "Sonic", "Pulse", "Tornado", "Quantum",
    "Momentum", "Nebula", "Bolt", "Ignition", "Rogue", "Vector", "Legend", "Ascendant", "Xperience",
    "Quantum", "Magnet", "Nova", "Xcel", "Maverick", "Titan", "Surge", "Maximus", "Vibe",
    "Spectra", "Storm", "Arcade", "Zen", "Vortex", "Omega", "Apollo", "Velocity", "Firestorm",
    "Titan", "Mirage", "Rift", "Horizon", "Chronos", "Legend", "Helix", "Dynamo", "Titanium",
    "Prism", "Fusion", "Blaze", "Ascend", "Hypernova", "Blitz", "Solaris", "Mirage", "Bolt",
    "Chroma", "Flare", "Excalibur", "Nebula", "Techno", "Glide", "Strike", "Hyperdrive", "Quantum",
    "Xeno", "Shockwave", "Hyperlink", "Astro", "Chrono", "Blast", "Vision", "Eclipse", "Zenith",
    "Circuit", "Hexa", "Phoenix", "Fusion", "Hyperlink", "Vanguard", "Perimeter", "Hyperpulse",
    "Onyx", "Aether", "Nirvana", "Enigma", "Revolva", "Magma", "Celestia", "Orbital", "Nebula",
    "Zeta", "Xeno", "Arcadia", "Dynamo", "Blaze", "Titan", "Streamline", "Gravitas", "Pulse",
    "Fission", "Frenzy", "Fusion", "Nebula", "Catalyst", "Zen", "Outlaw", "Void", "Orbit",
    "Titanium", "Mirage", "Radial", "Monolith", "Vortex", "Pulsar", "Forge", "Rift", "Flux",
    "Omni", "Thunder", "Vortex", "Stellar", "Storm", "Phantom", "Celestial", "Momentum", "Velocity",
    "Astro", "Vanguard", "Skyline", "Circuit", "Exosphere", "Infinity", "Perception", "Delta",
    "Volt", "Quantum", "Surge", "Nova", "Prism", "Hyperstorm", "Reflex", "Vibe", "Matrix",
    "Element", "Cosmic", "Galactic", "Pulse", "Orbit", "Horizon", "Spire", "Titan", "Force",
    "Genesis", "Meteor", "Falcon", "Nebula", "Solar", "Gravitation", "Impulse", "Skyward", "Aura"
]

# A list of 200 suffixes to use when making platform names. I got this list from ChatGPT
suffix_lst = [
    "Station", "System", "Core", "Platform", "Box", "Arena", "Drive", "Hub", "Link", "Unit",
    "Vault", "Edge", "Network", "Zone", "Stream", "X", "Deck", "Force", "Matrix", "Channel",
    "Grid", "Sphere", "Nexus", "Base", "Lab", "World", "Verse", "Cave", "Point", "Dock", "Channel",
    "Space", "Realm", "Gate", "Deck", "Hive", "Arena", "Dock", "Cluster", "Dome", "Matrix", "Base",
    "Field", "Vortex", "Stream", "Circuit", "Tower", "Node", "Pulse", "Station", "Field", "Node",
    "Arc", "Core", "Pulse", "Peak", "Territory", "Hub", "Zone", "Array", "Sphere", "Link", "Vibe",
    "System", "Pulse", "Cortex", "Forge", "Origin", "Infinity", "Runner", "Chamber", "Haven", "Boost",
    "Vision", "Grid", "Zone", "Link", "Path", "Network", "Node", "Xperience", "Matrix", "Titan",
    "Flash", "Circuit", "Turbine", "Nova", "Connect", "Crest", "Trek", "Edge", "Vista", "Access",
    "Fusion", "Spark", "Drive", "Nexus", "Tonic", "Crossover", "Bolt", "Interactive", "Vibe", "Deck",
    "Zeta", "Evolution", "Focus", "Core", "Platform", "Junction", "Insight", "Channel", "Next", "Vertex",
    "Orb", "Chrono", "Echo", "Voyage", "Phase", "Point", "Shift", "Vanguard", "Terra", "Scape", "Ultra",
    "Stream", "Pathway", "Impact", "Globe", "Plex", "Sphere", "Crossover", "Boost", "Circuit", "Prime",
    "Drift", "Edge", "Focus", "Mesh", "Jump", "Channel", "Arcade", "Horizon", "Hub", "Quark", "Sky",
    "Path", "Velocity", "Dynamo", "Vault", "Circuit", "Lab", "Catalyst", "Launch", "Space", "Peak",
    "Rift", "Venture", "Track", "Pulse", "Helix", "Stream", "Trek", "Vista", "Xperience", "Factor",
    "Nexis", "Nucleus", "Blaze", "Journey", "Terra", "Link", "Zone", "Exo", "Xpert", "Launch", "Jump",
    "Beacon", "Quantum", "Ranger", "Loop", "Drive", "Sector", "Infinity", "Skye", "Xenon", "Zonex",
    "Vortex", "Echelon", "Impulse", "Harbinger", "Sync", "Lift", "Orbit", "Voyage", "Vanguard", "Volt"
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

# Creates a new platform name by randomly choosing a prefix and randomly
# choosing a suffix, then putting them together in 1 fake platform name.
# The platform names are stored in a set to ensure they are unique.
def generate_platform_name():
    prefix = random.choice(prefix_lst)
    suffix = random.choice(suffix_lst)
    return prefix + " " + suffix




# to make an attempt to reconnect the database
# originally written by KIFEKACHUKWU NWOSU in collection.py
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn

# Function to insert the created user data onto the server
def insert_platforms_data(platform_lst, MAX_RETRIES):
    attempts = 0
    # a while loop and counter so we don't keep trying to connect to the database over and over again
    while attempts < MAX_RETRIES:
        connection = get_db_connection()
        if connection is None:
            print("Couldn't connect to the database.")
            return

        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO PLATFORM (name) VALUES (%s)"

                # inserting the items individually bc I could not get a bulk insert to work
                for item in platform_lst:
                    cursor.execute(insert_query, (item,))

                connection.commit()  # Commit once after all inserts
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
            return

        finally:
            if connection:
                connection.close()

    #let the user know if we ran out of tries to connect to the database
    print("Max retries reached. Could not create collection.")


# executes the process of adding user data by calling above functions

def main():
    platform_lst = []
    while len(platform_lst) < (15000):
        platform_lst.append((generate_platform_name(), ))
    insert_platforms_data(platform_lst, MAX_RETRIES)

main()







