# FastAPI Identity Service

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Alembic](https://img.shields.io/badge/Migrations-Alembic-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A production-style authentication and identity service built with FastAPI, PostgreSQL, and JWT.

This project is designed with a clean layered architecture and focuses on authentication workflows, database integration, environment-based configuration, and API scalability. It is intended as a backend learning project built with production-oriented development practices in mind.

---

## Features

- User registration
- User login
- JWT-based authentication
- Protected user endpoints
- Password hashing and verification
- Database integration with PostgreSQL
- Database migrations with Alembic
- Environment-based configuration
- Layered project structure using service and repository patterns
- Middleware support for cross-origin requests
- Automated API testing with Pytest
- Docker-ready development workflow

---

## Tech Stack

- FastAPI
- Python
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT
- Pytest
- Docker

---

## Project Structure

````text
project-root/
├── api/                 # API application versions
│   ├── v1/
│       ├── auth_v1.py   # FastAPI application entry point
├── app/
│   ├── routers/         # API routes
│   ├── services/        # business logic layer
│   ├── repositories/    # data access layer
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── core/            # config, security, cookies, dependencies,database setup
│
├── migrations/          # migration files
├── tests/               # automated tests
├── docker/              # Docker-related files
│   ├── Dockerfile
│   ├──.dockerignore
│   └── docker-compose.yml
├── requirements.txt
├── .env.sample
├── alembic.ini
├── .gitignore
└── README.md

---

## Architecture

This project follows a layered architecture to keep responsibilities separated and the codebase easier to maintain.

- Routers handle HTTP requests and responses
- Services contain business logic
- Repositories manage database operations
- Schemas define request and response validation
- Models represent database tables
- Core contains configuration, security, cookies, dependencies, and database setup

This structure improves readability, testability, and scalability as the project grows.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/glbvnd/fastAPI_jwt_service.git
cd fastAPI_jwt_service
````

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

On Linux/macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local environment file:

```bash
cp .env.sample .env
```

Example configuration:

```env
SQLALCHEMY_DATABASE_URL= postgresql://user:password@localhost:5432/auth_db
JWT_SECRET_KEY= supersecretkey
ACCESS_TOKEN_EXPIRE_MINUTES= 15 #minuts
REFRESH_TOKEN_EXPIRE_DAYS= 7 #days
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the application

```bash
uvicorn api.v1.auth_v1:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/swagger
```

---

## API Documentation

The API provides interactive documentation and endpoint testing through Swagger UI.

You can explore and test authentication endpoints directly at:

```text
http://127.0.0.1:8000/swagger
```

---

## API Endpoints

### Register

```http
POST /auth/register
```

Example request body:

```json
{
  "email": "user@example.com",
  "username": "testuser",
  "password": "strongpassword"
}
```

### Login

```http
POST /auth/login
```

Example response:

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

### Current User

```http
GET /auth/me
```

Example header:

```http
Authorization: Bearer <access_token>
```

---

## Middleware

The project includes CORS middleware for handling cross-origin requests.

Example configuration:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Notes

- `CORSMiddleware` is integrated into the application
- CORS settings should be different for development and production
- In production, `allow_origins` should contain only trusted frontend domains
- Credential-based requests should be enabled only when required by the authentication flow

---

## Production Readiness

This project is built with several production-oriented ideas in mind, even if some parts are still under active development.

### Implemented or Intended Practices

- Layered architecture for maintainability
- Environment-based configuration
- Secure JWT authentication flow
- Password hashing
- Migration-based database schema management
- Middleware-based request handling
- Testable project structure

### Recommended Production Setup

- Restrict CORS origins to trusted domains
- Store secrets in environment variables
- Never commit `.env` files or credentials
- Use HTTPS in deployment
- Use `HttpOnly`, `Secure`, and `SameSite` cookie settings if cookies are used for authentication
- Run the application behind a reverse proxy such as Nginx
- Add structured logging and monitoring
- Add rate limiting for authentication endpoints
- Add refresh token rotation if using long-lived sessions

---

## Running Tests

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

---

## Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "describe your change"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback the last migration:

```bash
alembic downgrade -1
```

---

## Docker

To build and run the project with Docker:

```bash
docker-compose up --build
```

If your project uses a different Docker setup, update this section accordingly.

---

## Environment Variables

| Variable                      | Description                        |
| ----------------------------- | ---------------------------------- |
| `DATABASE_URL`                | PostgreSQL connection string       |
| `SECRET_KEY`                  | Secret key used to sign JWT tokens |
| `ALGORITHM`                   | JWT signing algorithm              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration time       |

---

## Screenshots

### Swagger UI

![Swagger UI](./routers.png)

### Register Endpoint

![Register](./register.png)

### Login Endpoint

![Login](./login.png)

### Protected Route

![Protected Route](./me.png)

### Schemas

![Schemas](./docs/screenshots/schemas.png)

---

## Development Notes

This project is being developed as a learning-focused backend service with real-world architectural practices. The goal is not only to implement authentication features, but also to build the project in a maintainable, testable, and deployment-friendly way.

---

## License

This project is licensed under the MIT License.

```

```
