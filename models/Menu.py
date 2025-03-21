from db import get_db_connection
import collection
from user import User


userinput = ""
conn = get_db_connection()
def main():

    while True:
        print("\nWelcome to the Video Game!")
        print("Please sign in or create account with the folloeing commands: ")
        print("\n1. Create User")
        print("2. Login User")
        print("9. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            print("Taking you to Create a User...")
            User.create_account()
            # add relevant methods here
        elif choice == '2':
            print("Taking you to login... ")
            # add relevant methods here
            User.login()
        elif choice == '9':
            exit()
        else:
            print("Invalid option. Try again.")
            User.print_begin_menu()
        



if __name__ == '__main__':
    main()