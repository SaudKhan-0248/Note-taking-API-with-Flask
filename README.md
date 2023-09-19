# Note Taking API with Flask

This is a simple Note Taking API built using Flask. It allows users to perform various operations related to Notes management.

## Features

- User authentication (account creation, login, logout and account deletion)
- CRUD operations on notes (Create, Read, Update, Delete)
- Interactive API documentation with Swagger UI

## API Endpoints

### Authentication

- `POST /auth/signup`: Create a new user account.
- `POST /auth/login`: Log in with an existing user account.
- `DELETE /auth/logout`: Log out of the account.

### Notes

- `POST /notes/create`: Create a new note.
- `GET /notes`: Get all notes.
- `GET /notes/<title>`: Get a specific note by Note's title.
- `PUT /notes/update/<title>`: Update a specific note by Notes's title.
- `DELETE /notes/delete/<title>`: Delete a specific note by Note's title.

### User Account

- `GET /user/profile`: Get the user's Profile
- `DELETE /user/delete`: Delete the user account  

### API Documentation

The interactive API documentation is available at `/api/docs` using Swagger UI. You can use this interface to explore and test the API endpoints.

## Getting Started

To get started with this project:

#### Prerequisites

- Python 3.x
- Docker
- Docker-compose

#### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/note-taking-api.git
cd note-taking-api
```
2. Create a .env file in `src` directory and configure the necessary environment variables including `SECRET KEY, SQLALCHEMY_DATABASE_URL, JWT_SECRET_KEY` and `REDIS_HOST`
3. Build and run Docker containers using docker-compose
```bash
docker-compose up
```
4. Access the API at `http://localhost:5000`
5. Access the API's interactive documentation at `http://localhost:5000/api/docs`
