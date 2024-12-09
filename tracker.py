from datetime import datetime


class HealthMetrics:
    def __init__(self, db):
        """
        Initialize with a database connection.
        """
        self.db = db

    def add_metrics(self, user_id, weight, steps, water):
        """
        Add health metrics for a user on a specific date.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            self.db.add_health_metrics(user_id, today, weight, steps, water)
            print(f"Health metrics for {today} added successfully!")
        except Exception as e:
            print(f"An error occurred while adding health metrics: {e}")

    def view_metrics(self, user_id):
        """
        Retrieve and display all health metrics for a user.
        """
        try:
            return self.db.get_health_metrics(user_id)
        except Exception as e:
            print(f"An error occurred while retrieving health metrics: {e}")
            return []


class MedicationReminder:
    def __init__(self, db):
        """
        Initialize with a database connection.
        """
        self.db = db

    def add_reminder(self, user_id, medication, reminder_time):
        """
        Add a medication reminder for a user.
        """
        try:
            self.db.add_medication_reminder(user_id, medication, reminder_time)
            print(f"Reminder for {medication} at {reminder_time} added successfully!")
        except Exception as e:
            print(f"An error occurred while adding a medication reminder: {e}")

    def view_reminders(self, user_id):
        """
        Retrieve and display all medication reminders for a user.
        """
        try:
            return self.db.get_medication_reminders(user_id)
        except Exception as e:
            print(f"An error occurred while retrieving medication reminders: {e}")
            return []
