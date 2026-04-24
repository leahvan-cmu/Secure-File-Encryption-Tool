# A login system for users to access the tool, and store the password hash in csv file to authenticate users when they log in

import hashlib 
import secrets
import csv
import logging 

# set up log file for logins, append only 
logging.basicConfig(
    filename='audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# takes user input of username and password, hashes the password with a salt, and stores the username and hashed password in a csv file
def create_user():
    username = input("Create a username: ")
    password = input("Create a password: ")
    salt = secrets.token_bytes(16)
    # creates unique salt for each new account
    pwd_bytes = salt + password.encode('utf-8') 
    # hashes the password with the salt using sha256, and stores the username, salt, and hashed password in a csv file
    hashed_pwd = hashlib.sha256(pwd_bytes).hexdigest()
    with open('users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, salt.hex(), hashed_pwd]) 
# add to the log 
    logging.info(f"New user created: {username}")

# takes user input of username and password, hashes the password with the same salt, and checks if the hash matches the stored hash in the csv file
def login():
    with open('users.csv', mode='r') as file:
        reader = csv.reader(file)
        users = {rows[0]: (rows[1], rows[2]) for rows in reader}
    username = input("Username: ")
    password = input("Password: ")
    salt = bytes.fromhex(users[username][0]) 
    
    pwd_bytes = salt + password.encode('utf-8')
    hashed_pwd = hashlib.sha256(pwd_bytes).hexdigest()

    if username in users and secrets.compare_digest(hashed_pwd, users[username][1]):
        print("Welcome back, " + username)
        logging.info(f"Successful login: {username}")
    else:
        print("Incorrect password, please try again")
        logging.warning(f"Failed login attempt: {username}")

