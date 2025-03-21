import psycopg2
from db import get_db_connection
from collection import printCollectionsMenu

userinput = ""
conn = get_db_connection()
def main():
    print("Welcome to the Video Game Vault")

    while True:
        print("0️⃣: Reprint the Menu menu 🔄")
        print("2️⃣. Login User 🔑")
        print("3️⃣. View Video Game Menu 📋")
        print("4️⃣. View Collections Menu 📂")
        print("5️⃣. Exit 🚪")
        choice = input("Enter your choice: ")
        if choice == '1':
            print("Taking you to Create a User... 📝")
        elif choice == '2':
            print("Taking you to login... 🔑")
        elif choice == '3':
            print("Taking you to Video Game Menu... 🎮")
        elif choice == '4':
            print("Taking you to Collections Menu... 📂")
            printCollectionsMenu()
        elif choice == '5':
            print("Exiting... 👋")
            break


if __name__ == '__main__':
    main()