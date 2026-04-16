# Secure File Encryption and Decryption Tool
# 4/17/2026

def main():
    print("Secure File Encryption Tool")
    while True:
        print("1. Create User")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            create_user()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again")
