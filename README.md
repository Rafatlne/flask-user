# Flask User Management Application

This is a Flask application for managing user information, including CRUD operations on users, authentication, and user search functionality.

## Features

- **User Management**: Allows users to create, update, delete, and view user information.
- **Authentication**: Provides token-based authentication for securing API endpoints.
- **Search Functionality**: Enables users to search for users based on certain criteria.

## Prerequisites

- Python 3.10 or higher installed
- Docker (optional, for running with Docker)

# Setup

## 1. Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/flask-user-management.git

2. Navigate to the project directory:
    ```bash
    cd flask-user-management
3. Install dependencies:
    ```bash
    pip install -r requirements.txt

## 2. Configuration

- Set environment variables in a `.env` file or configure them directly in the environment. Required variables include:
    - FLASK_APP: manage.py.
    - CONFIG_ENV: Environment configuration (e.g., dev, prod).
    - FLASK_RUN_PORT: 8010
    - POSTGRES_USER=postgres # if you use docker
    - POSTGRES_PASSWORD=postgres # if you use docker
    - POSTGRES_HOST=db
    - POSTGRES_DB=flask_user
   
## 3. Usage

1. Start the Flask application:
    ```bash
    python -m flask run
   ```
    Alternatively, if you have Docker installed, you can use the provided Docker Compose file:
    ```bash
    docker-compose up
2. Access the API via http://localhost:8010 in your browser or using a tool like Postman.

## 4. Database Migration and Seeding

1. Apply the migration to the database:
    ```bash
   flask db upgrade
2. To seed the database with initial data, run the following command
    ```bash
   python seeder.py

## 5. API Documentation

The API documentation is available at http://localhost:8010/doc/ endpoint when the application is running. It provides detailed information on available endpoints, request parameters, and response formats.

## 6. Obtaining a Token with Basic Authentication

To obtain a token for authentication, you can use curl to make a POST request to `/auth/` with Basic Authentication using your username and password.

### Admin Credentials
    ```bash
    username: admin
    password: admin@123

### Request

```bash
curl -X POST \
  -H "Authorization: Basic $(echo -n 'admin:admin@123' | base64)" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin@123"}' \
  http://localhost:8010/auth/
