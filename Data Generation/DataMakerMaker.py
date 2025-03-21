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

# A list of 200 prefixes to use when making maker names. I got this list from ChatGPT
prefix_lst = ["Titan", "Pixel", "Quantum", "Hyper", "Cyber", "Retro", "Arcane", "Stellar", "Infinite", "Vortex",
    "Phantom", "Apex", "Neon", "Shadow", "Obsidian", "Lunar", "Cosmic", "Turbo", "Void", "Zenith",
    "Echo", "Catalyst", "Omicron", "Drift", "Flux", "Pulse", "Helix", "Nova", "Nebula", "Storm",
    "Glitch", "Warp", "Horizon", "Spectra", "Radiant", "Evolve", "Ascend", "Ignite", "Phoenix", "Omega",
    "Stratos", "Nimbus", "Vector", "Singularity", "Impulse", "Vertex", "Gravitas", "Perigee", "Orbit", "Polaris",
    "Enigma", "Chrono", "Mythic", "Sentinel", "Cipher", "Exo", "Genesis", "Tectonic", "Celestial", "Nexus",
    "Velocity", "Comet", "Solstice", "Dream", "Mirage", "Dynamo", "Tempest", "Legacy", "Arcadia", "Odyssey",
    "Frontier", "Echelon", "Kinetic", "Metronome", "Aurora", "Symphony", "Synergy", "Stormlight", "Prism", "Tundra",
    "Halcyon", "Ether", "Everest", "Veridian", "Eldritch", "Monarch", "Rune", "Sage", "Havoc", "Aspire",
    "Rogue", "Horizon", "Zen", "Gale", "Sol", "Crimson", "Elemental", "Oblivion", "Providence", "Colossus",
    "Echoes", "Celestia", "Astralis", "Circuit", "Spiral", "Prime", "Supernova", "Luminous", "Ember", "Auric",
    "Oracle", "Epoch", "Aeon", "Utopia", "Stormfront", "Paragon", "Aphelion", "Vanguard", "Ironclad", "Eclipse",
    "Atlas", "Pinnacle", "Quasar", "Solara", "Radiance", "Thermal", "Warped", "Tecton", "Astral", "Surge",
    "Pandora", "Neural", "Epochal", "Phenom", "Momentum", "Vertigo", "Tornado", "Sonic", "Fission", "Trailblazer",
    "Mystic", "Expanse", "Vivid", "Evolve", "Innovation", "Beacon", "Primeval", "Fluxion", "Neuron", "Prophet",
    "Infinitum", "Continuum", "Stormbringer", "Cataclysm", "Hyperion", "Chronicle", "Orion", "Skybound", "Circuitry", "Umbra",
    "Nocturne", "Auric", "OmegaCore", "Inferno", "Synth", "Envision", "Magnetar", "Vigilant", "Throne", "Harmonic",
    "Resonance", "Hypersonic", "Momentum", "Virtua", "Metaflux", "Omni", "Neonwave", "Aftershock", "Obscura", "ArcLight",
    "Neptune", "Archetype", "Mnemonic", "Pulsewave", "EchoTech", "Superposition", "Ion", "CatalystX", "Xenon", "Krypton",
    "Reactor", "Astralis", "Solarwind", "Helion", "Megabyte", "Bitstream", "ByteShift", "Lumen", "Metagalactic", "Spectral",
    "WarpDrive", "Neurobyte", "Fusion", "Singularis", "Straylight", "Aether", "Dreamforge", "VortexCore", "Altair", "Axion",
    "Heliopause", "Photon", "Stargazer", "Cloudburst", "InfiniteLoop", "Parallel", "Infinitron", "Magneto", "DarkMatter", "ZeroPoint",
    "Proxima", "Redshift", "Parallax", "Seraph", "Nebularis", "Exodus", "PrimeMover", "Solarflare", "Cybernetic", "Perseus",
    "DarkStar", "Crux", "Polymorphic", "Nautilus", "Tesseract", "Synaptic", "Bitstorm", "VertexX", "Inertia", "Hyperdrive",
    "Tesla", "Photonix", "HorizonX", "Psyche", "Cosmotic", "Draconis", "Lunarwave", "Voidwave", "SingularityX", "EventHorizon",
    "Techwave", "Pulsar", "EchelonX", "Cyberwave", "QuantumForge", "MetronX", "RedNova", "InfinityCore", "Neutron", "Planetfall",
    "SuperCluster", "Retrograde", "DarkHorse", "Everlight", "OmegaShift", "CyberSphere", "NeuroNova", "UltraCore", "CyberMind", "Macrocosm"
]

# A list of 250 suffixes to use when making platform names. I got this list from ChatGPT
suffix_lst = [
    "Studios", "Interactive", "Entertainment", "Games", "Productions", "Digital", "Softworks", "Software", "Works",
    "Inc.", "Creations", "Labs", "Network", "Forge", "Collective", "Systems", "Dynamics", "Pixelworks", "Media",
    "Innovations", "Vision", "Minds", "Industries", "Technologies", "Developments", "Creations", "Outpost",
    "Designs", "Machine", "Works", "Agency", "Initiative", "Core", "Projects", "Enterprises", "Unit", "Console",
    "Mechanics", "Engine", "Makers", "Craft", "Syndicate", "Frontier", "Nexus", "Arcade", "Chronicles", "Play",
    "Pixel", "Reality", "League", "Motion", "Crafters", "Engineers", "Simulation", "Odyssey", "Infinity",
    "Dynasty", "Legends", "Heroes", "Villains", "Glitch", "Matrix", "Code", "Tech", "Vanguard", "Division",
    "Blueprint", "Guild", "Alliance", "Circuit", "Prototype", "Hyper", "Impulse", "Protocol", "Virtual",
    "Dreams", "Quest", "Explorers", "Masters", "Rogue", "Strikers", "Storm", "Strike", "Rise", "Front",
    "Anomaly", "Cyber", "Dimension", "Generation", "Metaverse", "Synthetic", "AI", "Incursion", "Level",
    "Shadow", "Nebula", "Universe", "Arena", "Catalyst", "Outlaws", "Loadout", "Speedrun", "Rift", "Echo",
    "Havoc", "Override", "Mirage", "Divergence", "Faction", "Echelon", "Cipher", "Paragon", "Sentinel",
    "Monarch", "Stratos", "Elevate", "Entity", "Drift", "Continuum", "Cascade", "Warp", "Beacon", "Warpzone",
    "Expanse", "Stormfront", "Crusade", "Artifact", "Mode", "Vortex", "Luminary", "Ascend", "Momentum",
    "Pulse", "Evolve", "Synergy", "Epoch", "Vector", "Intelligence", "Construct", "Meta", "Hyperdrive",
    "Abyss", "Alpha", "Beta", "Gamma", "Omicron", "Radial", "Zenith", "Pinnacle", "Envision", "Nova",
    "Astralis", "Orbit", "Parallel", "Immersion", "Elevate", "Uplink", "Spire", "Threshold", "Infinity",
    "Crossroads", "Zero", "Legacy", "Titan", "Mythic", "Exodus", "Convergence", "Codebase", "Blueprints",
    "Gravity", "Runway", "Refinery", "Pathfinder", "Evolution", "Metamorph", "Axon", "Cogworks", "Horizon",
    "Digitality", "Prism", "Bolt", "Prime", "Havok", "Shift", "Spark", "Frame", "Cybernetics", "Algorithm",
    "Node", "Signal", "Beacon", "Stormworks", "Turbine", "Synergetic", "Axon", "Module", "Nebular", "Genesis",
    "Luminance", "Manifest", "Supernova", "Grid", "Quantum", "Schematic", "Renaissance", "Xenon", "Launchpad",
    "Kinetics", "Vectorworks", "Echoes", "Skyline", "Horizons", "Catalysts", "Zenworks", "Frameworks",
    "Simulationists", "Omniverse", "Neural", "Sentience", "Cyberdynamics", "Astromech", "Ultraviolet",
    "Tectonic", "Flashpoint", "Chrono", "Virtuality", "Pioneers", "Titanium", "Omniforge", "Aether",
    "Riftworks", "Starbound", "Synapse", "Lumina", "Algorithmics", "Celestial", "Pulsar", "Biome",
    "Intergalactic", "Hypernova", "Nomads", "Cryptic", "Warpdrive", "Oblivion", "Omnis", "Thresholds",
    "Pulseworks", "Digitalis", "Cryptoworks", "Neonworks", "Stormriders", "Xperience", "Spectral",
    "Inception", "Kaleidoscope", "Continuumworks", "Dreamforge"
]

# importing libraries
from faker import Faker  # This library that generates fake data
import time # so we can delay reconnect attempts
import psycopg2  # for connecting python and postgre
import random
from db import get_db_connection  # Ensure db.py is in the same directory/folder

# create a faker object and access Faker methods
fake = Faker()

# Creates a new platform name by randomly choosing a prefix and randomly
# choosing a suffix, then putting them together in 1 fake platform name.
# The platform names are stored in a set to ensure they are unique.
def generate_maker_name():
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
def insert_maker_data(maker_lst, MAX_RETRIES):
    attempts = 0
    # a while loop and counter so we don't keep trying to connect to the database over and over again
    while attempts < MAX_RETRIES:
        connection = get_db_connection()
        if connection is None:
            print("Couldn't connect to the database.")
            return

        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO MAKER (makername) VALUES (%s)"

                # inserting the items individually bc I could not get a bulk insert to work
                for item in maker_lst:
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
    maker_lst = []
    while len(maker_lst) < (15000):
        maker_lst.append((generate_maker_name(), ))
    insert_maker_data(maker_lst, MAX_RETRIES)

main()







