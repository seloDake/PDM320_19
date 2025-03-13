def main():
    print("Welcome to the Video Game Vault")

    while True:
        print("\n1. Create User")
        print("2. Login User")
        print("3. Add Video Game")
        print("4. List Video Games")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            email = input("Enter email: ")
            password = input("Enter password: ")
        elif choice == '2':
            email = input("Enter email: ")
            password = input("Enter password: ")
        elif choice == '3':
            name = input("Enter video game name: ")
            platform = input("Enter platform: ")
            developer = input("Enter developer: ")
            release_date = input("Enter release date (YYYY-MM-DD): ")

if __name__ == '__main__':
    main()