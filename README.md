# Hackathon Management API

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)

A robust, high-performance RESTful API built to manage the entire lifecycle of a hackathon. From participant registration and team formation to project submissions and judging criteria, this API handles the core backend logic required to run seamless technical events.

## 🚀 Tech Stack

* **Framework:** FastAPI (Python)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy / SQLModel
* **Containerization:** Docker & Docker Compose
* **Authentication:** JWT (JSON Web Tokens)
* **Data Validation:** Pydantic

## ✨ Core Features

* **User Management:** Secure registration and RBAC (Role-Based Access Control) for Participants, Mentors, Judges, and Admins.
* **Team Formation:** Endpoints to create teams, generate invite links, and manage team capacities.
* **Event Scheduling:** Track hackathon timelines, submission deadlines, and presentation slots.
* **Project Submissions:** Secure endpoints for submitting GitHub repositories, demo links, and architectural flowcharts.
* **Judging & Scoring:** Automated calculation of judge scores based on predefined criteria (e.g., Innovation, UI/UX, Technical Complexity).

## 🛠️ Local Development Setup

Follow these steps to get the API running locally. 

### Prerequisites
* Docker and Docker Compose installed on your machine.
* Git

### 1. Clone the Repository
```bash
git clone [https://github.com/iNaitik/hackathon_management_api.git](https://github.com/iNaitik/hackathon_management_api.git)
cd hackathon_management_api
