ToDo API with Django REST Framework

A simple RESTful API for managing a ToDo list using Django REST Framework and PostgreSQL.

🚀 Features

User registration and JWT authentication

Task CRUD (Create, Read, Update, Delete)

Task ownership and authorization

Mark tasks as completed

Filter tasks by status

Pagination for task listing

PostgreSQL database

Dockerized setup

Unit tests for API endpoints

📦 Installation

1. Clone the repository

git clone https://github.com/yourusername/todo_api.git
cd todo_api

2. Create .env (optional)

Configure environment variables if needed (only for advanced setups).

3. Docker setup

docker compose up --build

App will run at http://localhost:8000/

4. Or run locally without Docker

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

🧪 Running Tests

python manage.py test

(if using docker)
docker-compose exec web python manage.py test

🔐 Authentication

Uses JWT (JSON Web Tokens).

Obtain tokens

POST /api/token/
{
  "username": "your_username",
  "password": "your_password"
}

Use the access token

Add to request headers:

Authorization: Bearer <access_token>

🧾 API Endpoints

Auth

POST /api/token/ – get tokens

POST /api/token/refresh/ – refresh access token

Users

POST /api/users/register/ – create user

Tasks

GET /api/tasks/ – list all tasks (paginated)

GET /api/tasks/user/ – list tasks for current user

GET /api/tasks/<id>/ – task detail

POST /api/tasks/ – create task

PUT /api/tasks/<id>/ – update task

DELETE /api/tasks/<id>/ – delete task

POST /api/tasks/<id>/complete/ – mark task as completed

GET /api/tasks/?status=Completed – filter tasks by status

⚙️ Tech Stack

Python 3

Django + Django REST Framework

PostgreSQL

Docker

🧑‍💻 Author

Shabnam Nazarli

📄 License

This project is licensed under the MIT License.

