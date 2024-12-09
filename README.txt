# Healthcare Tracker App

The Healthcare Tracker App is a Python-based application designed to help users manage their health metrics and medication schedules efficiently. With a modern and user-friendly interface, the app provides essential features like data visualization, medication reminders, and secure user authentication.

## Features

- **User Registration and Login**:
  - Securely register and log in with a unique username and password.
  - Passwords are hashed for security.

- **Health Metrics Management**:
  - Add daily health metrics such as weight, steps walked, and water intake.
  - View previously entered metrics in a clear and organized format.
  - Visualize trends in weight and other metrics using graphs.

- **Medication Reminders**:
  - Set reminders for medications with specific times.
  - View all scheduled reminders in an organized list.
  - Get desktop notifications when it's time to take medication.

- **Export Data**:
  - Export health metrics to a `.csv` file for easy sharing or analysis.

- **Data Visualization**:
  - View trends in your health metrics (e.g., weight trends) using `matplotlib` graphs.

- **Modern Interface**:
  - Built using `Tkinter` and `ttkbootstrap` for a sleek, user-friendly design.
  - Includes custom themes, a logo, and interactive navigation.

- **Extensibility**:
  - Modular design for easy feature addition and scalability.

## Installation

1. Clone the repository:
https://github.com/AladdinOsamaAlswaifi/healthcare_tracker

2. Navigate to the project directory:
cd healthcare_tracker

3. Install the required dependencies:
pip install -r requirements.txt

4. Run the application:
python main.py

## Requirements

- Python 3.7 or higher
- Libraries:
- `tkinter` (built-in with Python)
- `ttkbootstrap`
- `matplotlib`
- `plyer`
- `pandas`

Install the required libraries using:
pip install ttkbootstrap matplotlib plyer pandas

## Usage

- Register a new user or log in with an existing account.
- Add and track daily health metrics such as weight, steps, and water intake.
- Schedule medication reminders and receive desktop notifications.
- Export your data to `.csv` or visualize trends using built-in graphs.

## Screenshots (Optional)

- **Login Screen**: ![Login Screen](assets/login_screen.png)
- **Dashboard**: ![Dashboard](assets/dashboard.png)

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the app.
