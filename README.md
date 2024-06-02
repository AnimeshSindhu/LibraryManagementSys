Overview
Library Management System is a Django-based web application designed to manage library operations such as cataloging books, managing user accounts, and tracking book loans.

Features
User Authentication: Secure login and registration for users.
Book Management: Add, update, delete, and view books.
Loan Management: Track book loans and returns.
Admin Interface: Django admin for easy management of the library database.

Installation
Clone the Repository:
```bash
git clone https://github.com/AnimeshSindhu/LibraryManagementSys.git
cd LibraryManagementSys
```
Create a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`
```
Install Dependencies:
```bash
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary faker pytz sqlparse asgiref
```
Apply Migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
Run the Server:
```bash
python manage.py runserver
```
Usage
Access the application at `http://127.0.0.1:8000/\`.
Use the Django admin at `http://127.0.0.1:8000/admin/` to manage the library database.

Project Structure
LibraryManagementSys/: Main project directory.
Library/: Django app for library management.
db.sqlite3: SQLite database file.
manage.py: Django management script.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request.
