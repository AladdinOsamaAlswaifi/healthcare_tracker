import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import PhotoImage, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from plyer import notification
from datetime import datetime
from user import User
from tracker import HealthMetrics, MedicationReminder
from database import Database

# Initialize database and global variables
db = Database()
current_user_id = None


def main():
    # Create the main window
    root = ttk.Window(themename="darkly")
    root.title("Healthcare Tracker")
    root.geometry("600x700")

    # Add a logo
    try:
        logo = PhotoImage(file="assets/logo.png")
        ttk.Label(root, image=logo).pack(pady=10)
    except Exception as e:
        print(f"Logo not found: {e}")

    # Show the login screen
    login_screen(root)

    # Run the Tkinter event loop
    root.mainloop()


def clear_screen(root):
    """Clear all widgets from the window."""
    for widget in root.winfo_children():
        widget.destroy()


### LOGIN SCREEN ###
def login_screen(root):
    """Login and Registration screen."""
    clear_screen(root)

    ttk.Label(root, text="Login", font=("Helvetica", 24), bootstyle=PRIMARY).pack(pady=20)

    ttk.Label(root, text="Username:").pack()
    username_entry = ttk.Entry(root, width=30)
    username_entry.pack()

    ttk.Label(root, text="Password:").pack()
    password_entry = ttk.Entry(root, width=30, show="*")
    password_entry.pack()

    def login():
        username = username_entry.get()
        password = password_entry.get()
        user = User(username, password)
        global current_user_id
        db_user = db.get_user(username, user.password)
        if db_user:
            current_user_id = db_user[0]
            dashboard_screen(root)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register():
        username = username_entry.get()
        password = password_entry.get()
        user = User(username, password)
        if db.add_user(username, user.password):
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Username already exists.")

    ttk.Button(root, text="Login", command=login, bootstyle=SUCCESS).pack(pady=10)
    ttk.Button(root, text="Register", command=register, bootstyle=INFO).pack(pady=5)
    ttk.Button(root, text="Forgot Password?", command=lambda: reset_password_screen(root), bootstyle=SECONDARY).pack(pady=5)


### RESET PASSWORD SCREEN ###
def reset_password_screen(root):
    """Reset password screen."""
    clear_screen(root)

    ttk.Label(root, text="Reset Password", font=("Helvetica", 24), bootstyle=PRIMARY).pack(pady=20)
    ttk.Label(root, text="Username:").pack()
    username_entry = ttk.Entry(root, width=30)
    username_entry.pack()

    ttk.Label(root, text="New Password:").pack()
    password_entry = ttk.Entry(root, width=30, show="*")
    password_entry.pack()

    def reset():
        username = username_entry.get()
        new_password = password_entry.get()
        user = User(username, "")
        if user.reset_password(db, new_password):
            messagebox.showinfo("Success", "Password reset successfully!")
            login_screen(root)
        else:
            messagebox.showerror("Error", "Failed to reset password.")

    ttk.Button(root, text="Reset Password", command=reset, bootstyle=SUCCESS).pack(pady=5)
    ttk.Button(root, text="Back", command=lambda: login_screen(root), bootstyle=INFO).pack(pady=5)


### DASHBOARD SCREEN ###
def dashboard_screen(root):
    """Dashboard screen for managing features."""
    clear_screen(root)

    ttk.Label(root, text="Dashboard", font=("Helvetica", 24), bootstyle=PRIMARY).pack(pady=20)

    ttk.Button(root, text="Add Health Metrics", command=lambda: health_metrics_screen(root), bootstyle=SUCCESS).pack(pady=5)
    ttk.Button(root, text="View Health Metrics", command=lambda: health_metrics_view_screen(root), bootstyle=INFO).pack(pady=5)
    ttk.Button(root, text="View Weight Trends", command=lambda: weight_trends_screen(root), bootstyle=INFO).pack(pady=5)
    ttk.Button(root, text="Add Medication Reminder", command=lambda: medication_reminder_screen(root), bootstyle=SUCCESS).pack(pady=5)
    ttk.Button(root, text="View Medication Reminders", command=lambda: medication_reminder_view_screen(root), bootstyle=INFO).pack(pady=5)
    ttk.Button(root, text="Export Data", command=export_data, bootstyle=SECONDARY).pack(pady=5)
    ttk.Button(root, text="Logout", command=lambda: login_screen(root), bootstyle=DANGER).pack(pady=20)


### HEALTH METRICS SCREENS ###
def health_metrics_screen(root):
    """Screen for adding health metrics."""
    clear_screen(root)

    ttk.Label(root, text="Add Health Metrics", font=("Helvetica", 24), bootstyle=PRIMARY).pack(pady=20)

    ttk.Label(root, text="Weight (kg):").pack()
    weight_entry = ttk.Entry(root, width=30)
    weight_entry.pack()

    ttk.Label(root, text="Steps:").pack()
    steps_entry = ttk.Entry(root, width=30)
    steps_entry.pack()

    ttk.Label(root, text="Water Intake (L):").pack()
    water_entry = ttk.Entry(root, width=30)
    water_entry.pack()

    def save_metrics():
        try:
            weight = float(weight_entry.get())
            steps = int(steps_entry.get())
            water = float(water_entry.get())
            health_metrics = HealthMetrics(db)
            health_metrics.add_metrics(current_user_id, weight, steps, water)
            messagebox.showinfo("Success", "Health metrics added successfully!")
            dashboard_screen(root)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    ttk.Button(root, text="Save", command=save_metrics, bootstyle=SUCCESS).pack(pady=10)
    ttk.Button(root, text="Back", command=lambda: dashboard_screen(root), bootstyle=INFO).pack(pady=5)


def health_metrics_view_screen(root):
    """Screen for viewing health metrics."""
    clear_screen(root)

    ttk.Label(root, text="Health Metrics", font=("Helvetica", 24), bootstyle=PRIMARY).pack(pady=20)

    health_metrics = HealthMetrics(db)
    metrics = health_metrics.view_metrics(current_user_id)

    if metrics:
        for record in metrics:
            ttk.Label(root, text=f"Date: {record[2]}, Weight: {record[3]} kg, Steps: {record[4]}, Water: {record[5]} L").pack()
    else:
        ttk.Label(root, text="No health metrics found.").pack()

    ttk.Button(root, text="Back", command=lambda: dashboard_screen(root), bootstyle=INFO).pack(pady=20)


### WEIGHT TRENDS SCREEN ###
def weight_trends_screen(root):
    """Generate and display weight trends graph."""
    health_metrics = HealthMetrics(db)
    metrics = health_metrics.view_metrics(current_user_id)

    if metrics:
        dates = [record[2] for record in metrics]
        weights = [record[3] for record in metrics]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, weights, marker="o")
        plt.title("Weight Trends")
        plt.xlabel("Date")
        plt.ylabel("Weight (kg)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("No Data", "No health metrics available to show trends.")


### MEDICATION REMINDER SCREENS ###
def medication_reminder_screen(root):
    """Screen for adding medication reminders."""
    clear_screen(root)

    ttk.Label(root, text="Add Medication Reminder", font=("Helvetica", 24), bootstyle=PRIMARY).pack(pady=20)

    ttk.Label(root, text="Medication Name:").pack()
    medication_entry = ttk.Entry(root, width=30)
    medication_entry.pack()

    ttk.Label(root, text="Reminder Time (HH:MM):").pack()
    time_entry = ttk.Entry(root, width=30)
    time_entry.pack()

    def save_reminder():
        medication = medication_entry.get()
        reminder_time = time_entry.get()
        try:
            medication_reminder = MedicationReminder(db)
            medication_reminder.add_reminder(current_user_id, medication, reminder_time)
            messagebox.showinfo("Success", "Reminder added successfully!")
            dashboard_screen(root)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    ttk.Button(root, text="Save", command=save_reminder, bootstyle=SUCCESS).pack(pady=10)
    ttk.Button(root, text="Back", command=lambda: dashboard_screen(root), bootstyle=INFO).pack(pady=5)


def medication_reminder_view_screen(root):
    """Screen for viewing medication reminders."""
    clear_screen(root)

    ttk.Label(root, text="Medication Reminders", font=("Helvetica", 24), bootstyle=PRIMARY).pack(pady=20)

    medication_reminder = MedicationReminder(db)
    reminders = medication_reminder.view_reminders(current_user_id)

    if reminders:
        for reminder in reminders:
            ttk.Label(root, text=f"Medication: {reminder[2]}, Time: {reminder[3]}").pack()
    else:
        ttk.Label(root, text="No reminders found.").pack()

    ttk.Button(root, text="Back", command=lambda: dashboard_screen(root), bootstyle=INFO).pack(pady=20)


### EXPORT DATA ###
def export_data():
    """Export health metrics to a CSV file."""
    health_metrics = HealthMetrics(db)
    metrics = health_metrics.view_metrics(current_user_id)

    if metrics:
        df = pd.DataFrame(metrics, columns=["ID", "User ID", "Date", "Weight", "Steps", "Water"])
        file_path = f"health_metrics_{current_user_id}.csv"
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
    else:
        messagebox.showinfo("No Data", "No health metrics to export.")


if __name__ == "__main__":
    main()
