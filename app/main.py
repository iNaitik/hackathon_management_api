from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import auth, hackathon, leaderboard,teams,submisions,votes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

cors_origins = [
    "http://localhost:5500",
    "http://localhost:5000",
    "http://127.0.0.1:5500"
]
app.add_middleware(
  CORSMiddleware,
  allow_origins = cors_origins,
  allow_methods = ["*"],
  allow_headers = ["*"]
)

app.include_router(auth.router)
app.include_router(hackathon.router)
app.include_router(votes.router)
app.include_router(leaderboard.router)
app.include_router(teams.router)
app.include_router(submisions.router)