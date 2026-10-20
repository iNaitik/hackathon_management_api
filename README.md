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
DATABASE_URL=postgresql://postgres:your_password@postgres:5432/hackathon
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Use your own local development credentials. Never commit real passwords, API keys, or production secrets. The hostname `postgres` is the database service name defined in `docker-compose.yml`.

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

### Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

On Windows:

```powershell
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

### Run Database Migrations and Start the Server

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

## Testing

Install the project dependencies and pytest, then run:

```bash
pip install -r requirements.txt
pip install pytest
pytest
```

The GitHub Actions workflow also provisions a temporary PostgreSQL service and runs the test suite before publishing a production image.

## API Documentation

FastAPI automatically generates interactive API documentation after the server starts:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Docker Services

| Service | Description | Port |
| --- | --- | --- |
| `api` | FastAPI backend application | `8000` |
| `postgres` | PostgreSQL database | `5432` |

## Deployment

The API is deployed as a Docker image-backed Web Service on **Render**, using **Render PostgreSQL** for the production database. GitHub Actions builds the image and publishes it to Docker Hub; Render then pulls the image through its deploy hook.

### CI/CD Pipeline

```text
Developer pushes to GitHub
          |
          v
GitHub Actions CI
  - Python 3.12 setup
  - Install dependencies
  - Run pytest
          |
          | Only after CI succeeds,
          | and only on push to master
          v
Build Docker image (linux/amd64)
          |
          v
Push image to Docker Hub
  - latest tag
  - commit SHA tag
  - capture image digest
          |
          v
GitHub Actions CD
  - Trigger Render deploy hook
  - Pass the exact image digest
          |
          v
Render pulls and deploys that image
          |
          v
FastAPI + Render PostgreSQL
```

Workflow behavior:
- Pushes and pull requests run CI.
- Pull requests do not publish production images or trigger deployment.
- Only a push to `master` can publish the Docker image and trigger Render deployment.
- A failed test or image build prevents the deployment job from running.
- Render receives the image digest produced by the successful build, so the deploy hook targets that exact image rather than relying only on the mutable `latest` tag.
- The workflow uses GitHub Actions environment secrets for database/test configuration and Docker Hub credentials, plus `RENDER_DEPLOY_HOOK_URL` in the `Production` environment. Configure these secrets in the repository's GitHub Actions settings; do not put their values in the repository.

Database migrations (`alembic upgrade head`) are configured to run during container startup, before the FastAPI/Uvicorn server starts.

- **Live API:** [https://hackathon-management-api-sdqt.onrender.com](https://hackathon-management-api-sdqt.onrender.com)
- **Swagger/OpenAPI docs:** [https://hackathon-management-api-sdqt.onrender.com/docs](https://hackathon-management-api-sdqt.onrender.com/docs)

Local development remains separate and uses Docker Compose with its own PostgreSQL container.

## Future Improvements

- Judge roles and evaluation system
- Admin management features
- Team leave functionality

## Author

**Naitik**

Built as a backend engineering project to explore FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, Alembic migrations, and Docker-based development.
