from db import get_db_connection
import collection
from user import User


userinput = ""
conn = get_db_connection()
def main():

    while True:
        print("\n🎮 Welcome to the Game Vault! 🚀")
        print("Please sign in or create an account with the following commands:")
        print("\n1️⃣. Create User ✍️")
        print("2️⃣. Login User 🔑")
        print("9️⃣. Exit ❌")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Taking you to Create a User... ✍️")
            User.create_account()
        elif choice == '2':
            print("Taking you to login... 🔑")
            User.login()
        elif choice == '9':
            print("Exiting... 👋")
            exit()
        else:
            print("❌ Invalid option. Try again.")
            User.print_begin_menu()


if __name__ == '__main__':
    main()