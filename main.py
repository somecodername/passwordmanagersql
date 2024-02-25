import sqlite3
import re
import random
import string
import logging

# Setting up logging
logging.basicConfig(filename='password_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Password pattern for strength validation
password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS passwords
                     (website TEXT PRIMARY KEY, password TEXT)''')
        conn.commit()
    except sqlite3.Error as e:
        logging.error("An error occurred while creating the table: %s", e)

def add_password(conn):
    website = input("Enter website or service name: ")
    password = input("Enter password: ")
    
    try:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO passwords VALUES (?, ?)", (website, password))
        conn.commit()
        print("Password added successfully.")
        logging.info("Password added for %s", website)
    except sqlite3.Error as e:
        logging.error("An error occurred while adding the password: %s", e)

def retrieve_password(conn):
    website = input("Enter website or service name: ")
    
    try:
        c = conn.cursor()
        c.execute("SELECT password FROM passwords WHERE website=?", (website,))
        result = c.fetchone()
    
        if result:
            print("Password:", result[0])
            logging.info("Password retrieved for %s", website)
        else:
            print("Password not found.")
            logging.warning("Password not found for %s", website)
    except sqlite3.Error as e:
        print("An error occurred while retrieving the password:", e)
        logging.error("An error occurred while retrieving the password: %s", e)


def generate_password(strength):
    if strength == 'easy':
        length = 10
    elif strength == 'normal':
        length = 30
    elif strength == 'hard':
        length = 50
    else:
        return None
    
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_one_time_password(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def main():
    conn = None
    try:
        conn = sqlite3.connect('passwords.db')
        create_table(conn)  # Ensure the table exists

        while True:
            print("\nPassword Manager Menu:")
            print("1. Add Password")
            print("2. Retrieve Password")
            print("3. Generate One-Time Password")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                add_password(conn)
            elif choice == "2":
                retrieve_password(conn)
            elif choice == "3":
                length = int(input("Enter password length (max 16): "))
                if length > 16:
                    print("Password length cannot exceed 16 characters.")
                    continue
                password = generate_one_time_password(length)
                print("Generated one-time password:", password)
                logging.info("Generated one-time password with length %d", length)
            elif choice == "4":
                print("Exiting...")
                logging.info("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

    except sqlite3.Error as e:
        print("An error occurred with the database:", e)
        logging.error("Database error: %s", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
