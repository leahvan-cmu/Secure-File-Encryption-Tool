# Create login system for users to access the tool, and store the password hash in csv file to authenticate users when they log in


import hashlib 
import secrets
import sha256 
import csv
salt = secrets.token_bytes(16)

# takes user input of username and password, hashes the password with a salt, and stores the username and hashed password in a csv file
def create_user():
    username = input("Create a username: ")
    password = input("Create a password: ")
    pwd_salt = password + salt 
    hashed_pwd = hashlib.sha256(pwd_salt.encode()).hexdigest()
    with open('users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, hashed_pwd]) 

# takes user input of username and password, hashes the password with the same salt, and checks if the hash matches the stored hash in the csv file
def login():
    with open('users.csv', mode='r') as file:
        reader = csv.reader(file)
        users = {rows[0]: rows[1] for rows in reader}
    username = input("Username: ")
    password = input("Password: ")
    pwd_salt = password + salt 
    hashed_pwd = hashlib.sha256(pwd_salt.encode()).hexdigest()

    if username in users and hashed_pwd == users[username]:
        print("Welcome back, " + username)
    else:
        print("Incorrect password, please try again")

