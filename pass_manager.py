from cryptography.fernet import Fernet
import json

def generate_key():
  """Generates a new encryption key."""
  return Fernet.generate_key()

def load_key():
  """Loads the encryption key from a file."""
  try:
    with open("encryption_key.key", "rb") as key_file:
      return key_file.read()
  except FileNotFoundError:
    print("Encryption key file not found. Generating a new key.")
    key = generate_key()
    with open("encryption_key.key", "wb") as key_file:
      key_file.write(key)
    return key

def encrypt_password(password, key):
  """Encrypts the password using the provided key."""
  fernet = Fernet(key)
  encrypted_password = fernet.encrypt(password.encode())
  return encrypted_password.decode()

def decrypt_password(encrypted_password, key):
  """Decrypts the encrypted password using the provided key."""
  fernet = Fernet(key)
  decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
  return decrypted_password

def save_passwords(passwords, key):
  """Saves the encrypted passwords to a file."""
  with open("passwords.json", "w") as file:
    json.dump(passwords, file, indent=4)

def load_passwords(key):
  """Loads the encrypted passwords from a file."""
  try:
    with open("passwords.json", "r") as file:
      return json.load(file)
  except FileNotFoundError:
    return {}

def add_password(website, username, password, key):
  """Adds a new password to the password manager."""
  encrypted_password = encrypt_password(password, key)
  passwords = load_passwords(key)
  passwords[website] = {"username": username, "password": encrypted_password}
  save_passwords(passwords, key)
  print(f"Password for {website} added successfully.")

def retrieve_password(website, key):
  """Retrieves a password from the password manager."""
  passwords = load_passwords(key)
  if website in passwords:
    encrypted_password = passwords[website]["password"]
    username = passwords[website]["username"]
    decrypted_password = decrypt_password(encrypted_password, key)
    print(f"Username for {website}: {username}")
    print(f"Password for {website}: {decrypted_password}")
  else:
    print(f"No password found for {website}.")

def main():
  key = load_key()

  while True:
    print("\n--- Password Manager ---")
    print("1. Add a new password")
    print("2. Retrieve a password")
    print("3. Quit")
    choice = input("Enter your choice: ")

    if choice == '1':
      website = input("Enter the website or app name: ")
      username = input("Enter the username: ")
      password = input("Enter the password: ")
      add_password(website, username, password, key)
    elif choice == '2':
      website = input("Enter the website or app name: ")
      retrieve_password(website, key)
    elif choice == '3':
      print("Exiting the Password Manager.")
      break
    else:
      print("Invalid choice. Please try again.")

if __name__ == "__main__":
  main()