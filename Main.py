# Secure File Encryption and Decryption Tool
# Team Members: Avery Long, Leah VanNeste 
# 4/28/2026
from user_login import create_user, login
from file_hashing import save_hash, verify_hash


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
            
def file_menu():
    while True:
        print("\n1. Encrypt File")
        print("2. Decrypt File")
        print("3. Hash File")
        print("4. Verify Hash")
        print("5. Sign File")
        print("6. Verify Signature")
        print("7. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            encrypt_file(input("File path: "), input("Password: "))
        elif choice == '2':
            decrypt_file(input("File path: "), input("Password: "))
        elif choice == '3':
            save_hash(input("File path: "))
        elif choice == '4':
            verify_hash(input("File path: "))
        elif choice == '5':
            # when you finish Digital signature part, add the function for this here
        elif choice == '6':
            # when you finish Digital signature part, add the function for this here
        elif choice == '7':
            break
        else:
            print("Invalid choice, please try again")           
               
            

if __name__ == '__main__':
    main()