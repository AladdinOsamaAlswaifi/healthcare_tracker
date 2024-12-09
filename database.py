import sqlite3


class Database:
    def __init__(self, db_name="data/healthcare_tracker.db"):
        """
        Initialize the database connection and create tables if they don't exist.
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Create required tables for the application.
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            weight REAL,
            steps INTEGER,
            water REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS medication_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medication TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        self.conn.commit()

    # User Methods
    def add_user(self, username, password):
        """
        Add a new user to the database.
        """
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, username, password):
        """
        Retrieve a user from the database by username and password.
        """
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        return self.cursor.fetchone()

    # Health Metrics Methods
    def add_health_metrics(self, user_id, date, weight, steps, water):
        """
        Add health metrics for a user.
        """
        self.cursor.execute("""
        INSERT INTO health_metrics (user_id, date, weight, steps, water)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, date, weight, steps, water))
        self.conn.commit()

    def get_health_metrics(self, user_id):
        """
        Retrieve all health metrics for a user.
        """
        self.cursor.execute(
            "SELECT * FROM health_metrics WHERE user_id = ? ORDER BY date ASC",
            (user_id,),
        )
        return self.cursor.fetchall()

    # Medication Reminder Methods
    def add_medication_reminder(self, user_id, medication, reminder_time):
        """
        Add a medication reminder for a user.
        """
        self.cursor.execute("""
        INSERT INTO medication_reminders (user_id, medication, reminder_time)
        VALUES (?, ?, ?)
        """, (user_id, medication, reminder_time))
        self.conn.commit()

    def get_medication_reminders(self, user_id):
        """
        Retrieve all medication reminders for a user.
        """
        self.cursor.execute(
            "SELECT * FROM medication_reminders WHERE user_id = ?",
            (user_id,),
        )
        return self.cursor.fetchall()

    def close_connection(self):
        """
        Close the database connection.
        """
        self.conn.close()
