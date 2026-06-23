# 🚀 Hackathon Management API

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-green.svg)

A production-style backend API built with FastAPI and PostgreSQL to manage hackathons from team formation to project submissions, voting, and leaderboard generation.

## 🎯 Project Goal

This project was built to practice backend engineering concepts beyond basic CRUD operations, including authentication, relational database design, SQL aggregations, schema migrations, and business rule enforcement.

## ✨ Features

* **🔐 Authentication & Security:** User registration, secure login system, JWT-based authentication, and protected API endpoints.
* **👥 Team Management:** Create teams, join existing teams, enforce team capacity limits, and prevent multiple team memberships within the same hackathon.
* **🏆 Hackathon Management:** Create hackathons and associate teams with specific events.
* **📤 Project Submission System:** One submission per team, team member authorization checks, and storage for project information and links.
* **⭐ Voting System:** Score projects from 1–10, prevent duplicate voting, prevent self-voting, and enforce business rules directly at the API level.
* **📊 Dynamic Leaderboard:** Rank teams based on average scores, calculate vote statistics using SQL aggregations, and generate real-time leaderboards.

## 🛠 Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend Framework** | FastAPI |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Authentication** | JWT |
| **Validation** | Pydantic |
| **Migrations** | Alembic |
| **Language** | Python |

## 🎯 Key Concepts Demonstrated

* JWT Authentication & Authorization
* SQLAlchemy ORM Relationships
* One-to-Many and Many-to-Many Database Design
* Database Migrations with Alembic
* SQL Joins and Aggregations
* REST API Development
* Business Logic Validation

## 🗄 Database Architecture

### Core Entities & Relationships

```text
User
 │
 ├── Team_Member ──── Team ──── Hackathon
 │                      │
 │                      ▼
 │                 Submission
 │                      │
 └──────────── Vote ◄───┘

One Hackathon → Many Teams

One Team → One Submission

Many Users ↔ Many Teams

One Submission → Many Votes

📡 API Endpoints
Authentication
POST /register

POST /login

Hackathons
POST /hackathons

Teams
POST /teams

POST /teams/{id}/join

Submissions
POST /teams/{team_id}/submit

Voting
POST /submissions/{submission_id}/vote

Leaderboard
GET /hackathons/{hackathon_id}/leaderboard

🚀 Getting Started
Clone Repository
Bash
git clone [https://github.com/iNaitik/hackathon_management_api.git](https://github.com/iNaitik/hackathon_management_api.git)
cd hackathon_management_api
Create Virtual Environment
Bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
Install Dependencies
Bash
pip install -r requirements.txt
Configure Environment Variables
Create a .env file:

Code snippet
DATABASE_URL=postgresql://username:password@localhost/hackathon
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
Run Migrations
Bash
alembic upgrade head
Start Server
Bash
fastapi dev
API Documentation
FastAPI automatically generates interactive documentation. Once the server is running, visit:

Swagger UI: http://127.0.0.1:8000/docs

🔮 Future Improvements
Judge Roles & Evaluation System

Admin Dashboard

Team Leave Functionality

Docker Deployment

Automated Testing with Pytest

👨‍💻 Author
Naitik

Built as a backend engineering project to explore FastAPI, PostgreSQL, SQLAlchemy, JWT Authentication, and Alembic Migrations.


I kept "Docker Deployment" in the Future Improvements because wrapping this in a container is the logical next step for your backend progression anyway. 

Push the code, commit this README, add the bullet points to your resume, and shut this project down. You have squeezed the learning value out of it. Start scoping the ML project immediately.
