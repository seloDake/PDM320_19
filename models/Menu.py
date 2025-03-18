import psycopg2
from db import get_db_connection
from collection import printCollectionsMenu

userinput = ""
conn = get_db_connection()
def main():
    print("Welcome to the Video Game Vault")

    while True:
        print("\n1. Create User")
        print("2. Login User")
        print("3. View Video Game Menu")
        print ("4.View Collections Menu")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            print("Taking you to Create a User...")
            # add relevant methods here
        elif choice == '2':
            print("Taking you to login... ")
            # add relevant methods here

        elif choice == '3':
            print("Taking you to VideoGame Menu... ")
            # add relevant methods here
        elif choice == '4':
            printCollectionsMenu()



if __name__ == '__main__':
    main()