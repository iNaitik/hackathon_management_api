# Hackathon Management API

A REST API built with FastAPI and PostgreSQL to manage hackathons, teams, project submissions, voting, and leaderboards.

The project was developed to practice backend development concepts including authentication, database relationships, business logic implementation, SQL aggregations, and schema migrations.

---

## Features

### Authentication

* User Registration
* User Login
* JWT Authentication
* Protected Routes

### Hackathons

* Create Hackathons
* View Hackathon Details

### Teams

* Create Teams
* Join Existing Teams
* Team Capacity Validation
* Prevent Users from Joining Multiple Teams in the Same Hackathon

### Project Submissions

* Submit Project Details
* One Submission Per Team
* Restrict Submission Access to Team Members

### Voting System

* Vote on Project Submissions
* Score Range Validation (1–10)
* Prevent Duplicate Votes
* Prevent Users from Voting for Their Own Team

### Leaderboard

* Rank Teams by Average Vote Score
* Calculate Average Scores Using SQL Aggregations
* Count Total Votes Per Team
* Display Ordered Leaderboard Rankings

---

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication
* Alembic

---

## Database Design

### Tables

* Users
* Hackathons
* Teams
* Team_Members
* Submissions
* Votes

### Relationships

* One Hackathon → Many Teams
* One Team → One Submission
* Many Users ↔ Many Teams (through Team_Members)
* One Submission → Many Votes

---

## API Endpoints

### Authentication

| Method | Endpoint  |
| ------ | --------- |
| POST   | /register |
| POST   | /login    |

### Hackathons

| Method | Endpoint    |
| ------ | ----------- |
| POST   | /hackathons |

### Teams

| Method | Endpoint         |
| ------ | ---------------- |
| POST   | /teams           |
| POST   | /teams/{id}/join |

### Submissions

| Method | Endpoint                |
| ------ | ----------------------- |
| POST   | /teams/{team_id}/submit |

### Voting

| Method | Endpoint                          |
| ------ | --------------------------------- |
| POST   | /submissions/{submission_id}/vote |

### Leaderboard

| Method | Endpoint                               |
| ------ | -------------------------------------- |
| GET    | /hackathons/{hackathon_id}/leaderboard |

---

## Running Locally

### Clone Repository

```bash
git clone https://github.com/iNaitik/hackathon_management_api.git
cd hackathon_management_api
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

```bash
# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost/hackathon
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Run Database Migrations

```bash
alembic upgrade head
```

### Start Server

```bash
fastapi dev
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Concepts Demonstrated

* REST API Design
* JWT Authentication
* SQLAlchemy ORM Relationships
* PostgreSQL Integration
* Database Migrations with Alembic
* SQL Joins
* Aggregation Functions (AVG, COUNT)
* Business Logic Validation
* FastAPI Dependency Injection
