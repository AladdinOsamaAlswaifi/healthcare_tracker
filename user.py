import hashlib


class User:
    def __init__(self, username, password):
        """
        Initialize a User object with a username and hashed password.
        """
        self.username = username
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        """
        Hash the user's password using SHA-256 for secure storage.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, db):
        """
        Register a new user in the database.
        Returns True if registration is successful, False if the username already exists.
        """
        try:
            if db.add_user(self.username, self.password):
                print("User registered successfully!")
                return True
            else:
                print("Registration failed. Username already exists.")
                return False
        except Exception as e:
            print(f"An error occurred during registration: {e}")
            return False

    def login(self, db):
        """
        Log in the user by verifying the username and password with the database.
        Returns True if login is successful, False otherwise.
        """
        try:
            user = db.get_user(self.username, self.password)
            if user:
                print("Login successful!")
                return True
            else:
                print("Invalid username or password.")
                return False
        except Exception as e:
            print(f"An error occurred during login: {e}")
            return False

    def reset_password(self, db, new_password):
        """
        Reset the user's password.
        """
        try:
            hashed_password = self.hash_password(new_password)
            db.cursor.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (hashed_password, self.username),
            )
            db.conn.commit()
            return True
        except Exception as e:
            print(f"Error resetting password: {e}")
            return False
