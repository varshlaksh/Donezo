# Donezo - Task Management System

Donezo is a web-based task management system built with Django and Bootstrap. It allows users to manage, assign, and track tasks efficiently.

## Features

- 🔐 User Management
  - User registration and authentication
  - Role-based access control
  - Profile management

- 📋 Task Management
  - Create, edit, delete, and view tasks
  - Task attributes: Title, Description, Due Date, Priority, Status
  - Task assignment to team members

- 🔔 Notifications
  - Task assignment notifications
  - Deadline reminders
  - Real-time updates

- 🔎 Search & Filter
  - Search tasks by title or description
  - Filter by status, priority, due date, or assignee

- 📊 Dashboard
  - Task statistics
  - Performance metrics
  - Upcoming deadlines

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/donezo.git
cd donezo
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the application at `http://localhost:8000`
2. Register a new account or login with existing credentials
3. Start creating and managing tasks!

## Setting up Reminder Notifications

To set up automatic reminder notifications, add the following to your crontab (Linux/Mac) or Task Scheduler (Windows):

```bash
# Run every hour
0 * * * * cd /path/to/donezo && python manage.py send_reminders
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 