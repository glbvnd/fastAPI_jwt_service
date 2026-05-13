# FastAPI Identity Service

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A production‑style authentication service built with **FastAPI**, **PostgreSQL**, and **JWT**, following a **clean layered architecture**.  
This project demonstrates best practices for building scalable backend APIs including authentication, database migrations, containerization, and automated testing.

---

## Overview

This service provides a modular authentication system including:

- User registration
- Secure login
- JWT token generation
- Protected routes
- Database migrations
- Environment-based configuration

The architecture separates business logic, database access, and API layers to keep the codebase maintainable and scalable.

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT (JSON Web Tokens)
- Pydantic
- Pytest
- Docker

---

## Project Structure

```
project-root
│
├── app
│   ├── routers          # API routes
│   ├── services         # business logic
│   ├── repositories     # database access layer
│   ├── models           # SQLAlchemy models
│   ├── schemas          # Pydantic schemas
│   ├── core
│   │   ├── config.py    # environment settings
│   │   ├── database.py  # database session
│   │   └── security.py  # JWT & password hashing
│   │
│   └── main.py          # FastAPI application entry
│
├── alembic              # database migrations
├── alembic.ini
│
├── tests                # pytest tests
│
├── requirements.txt
├── .env
├── .env.sample
├── .gitignore
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```
git clone https://github.com/yourusername/fastapi-auth-service.git
cd fastapi-auth-service
```

---

### 2. Create virtual environment

```
python -m venv venv
```

Activate:

Linux / macOS

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create `.env` from the example:

```
cp .env.sample .env
```

Example configuration:

```
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 5. Run database migrations

```
alembic upgrade head
```

---

### 6. Start the API server

```
uvicorn app.main:app --reload
```

Server will start at:

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

---

## API Example

### Register User

```
POST /auth/register
```

Request:

```
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

Response:

```
{
  "id": 1,
  "email": "user@example.com"
}
```

---

### Login

```
POST /auth/login
```

Response:

```
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

### Access Protected Route

Header:

```
Authorization: Bearer <access_token>
```

---

## Running Tests

```
pytest
```

---

## Database Migrations

Create migration:

```
alembic revision --autogenerate -m "add user table"
```

Apply migration:

```
alembic upgrade head
```

---

## Docker

Build and run the project using Docker:

```
docker-compose up --build
```

---

## License

MIT License
