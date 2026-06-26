# Hackathon Management API

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

A production-style backend API built with FastAPI and PostgreSQL for managing hackathons, including team formation, project submissions, voting, and leaderboard generation.

## Project Goal

This project was built to practice backend engineering concepts beyond basic CRUD operations, including authentication, relational database design, SQL aggregations, schema migrations, Docker-based development, and business rule enforcement.

## Features

### Authentication and Security

- User registration
- Secure login system
- JWT-based authentication
- Protected API endpoints

### Team Management

- Create teams
- Join existing teams
- Validate team capacity
- Prevent multiple team memberships within the same hackathon

### Hackathon Management

- Create hackathons
- Associate teams with specific hackathons

### Project Submission System

- Allow one submission per team
- Verify team member authorization
- Store project information and links

### Voting System

- Score projects from 1 to 10
- Prevent duplicate voting
- Prevent self-voting
- Enforce business rules at the API level

### Dynamic Leaderboard

- Rank teams by average vote score
- Calculate vote statistics using SQL aggregations
- Generate real-time leaderboards

### Dockerized Development

- Dockerfile for containerizing the FastAPI application
- Docker Compose setup for the API and PostgreSQL database
- Persistent PostgreSQL storage using Docker volumes
- Environment-based configuration using `.env`

## Tech Stack

| Category | Technology |
| --- | --- |
| Backend Framework | FastAPI |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Validation | Pydantic |
| Migrations | Alembic |
| Containerization | Docker |
| Language | Python 3.12 |

## Key Concepts Demonstrated

- JWT authentication and authorization
- SQLAlchemy ORM relationships
- One-to-many and many-to-many database design
- Database migrations with Alembic
- SQL joins and aggregations
- REST API development
- Business logic validation
- Dependency injection with FastAPI
- Dockerized backend development
- PostgreSQL service orchestration with Docker Compose

## API Endpoints

### Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Authenticate a user and return a JWT |

### Hackathons

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/hackathons` | Create a new hackathon |

### Teams

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/teams` | Create a team |
| `POST` | `/teams/{id}/join` | Join an existing team |

### Submissions

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/teams/{team_id}/submit` | Submit a project for a team |

### Voting

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/submissions/{submission_id}/vote` | Vote on a submitted project |

### Leaderboard

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/hackathons/{hackathon_id}/leaderboard` | Get the hackathon leaderboard |

## Getting Started

### Prerequisites

Install the following tools before running the project:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)

### Clone the Repository

```bash
git clone https://github.com/iNaitik/hackathon_management_api.git
cd hackathon_management_api
```

## Run with Docker

Docker is the recommended way to run this project because it starts both the FastAPI application and PostgreSQL database together.

### Create Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:1353@postgres:5432/hackathon
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The hostname `postgres` is the database service name defined in `docker-compose.yml`.

### Build and Start Containers

```bash
docker compose up --build
```

This starts:

- FastAPI application on `http://127.0.0.1:8000`
- PostgreSQL database on port `5432`

### Run Database Migrations

In a separate terminal, run:

```bash
docker compose exec api alembic upgrade head
```

### Stop Containers

```bash
docker compose down
```

### Stop Containers and Remove Database Volume

Use this only when you want to reset the database completely:

```bash
docker compose down -v
```

## Local Development Without Docker

If you prefer running the project directly on your machine, install Python and PostgreSQL locally.

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

On Windows:

```bash
.venv\Scripts\activate
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/hackathon
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Run Database Migrations

```bash
alembic upgrade head
```

### Start the Development Server

```bash
uvicorn app.main:app --reload
```

## API Documentation

FastAPI automatically generates interactive API documentation after the server starts:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Docker Services

| Service | Description | Port |
| --- | --- | --- |
| `api` | FastAPI backend application | `8000` |
| `postgres` | PostgreSQL database | `5432` |

## Future Improvements

- Judge roles and evaluation system
- Admin management features
- Team leave functionality
- Automated testing with Pytest
- CI/CD integration
- Production deployment configuration

## Author

**Naitik**

Built as a backend engineering project to explore FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, Alembic migrations, and Docker-based development.
