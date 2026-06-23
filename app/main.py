from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import auth, hackathon, leaderboard,teams,submisions,votes

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(hackathon.router)
app.include_router(votes.router)
app.include_router(leaderboard.router)
app.include_router(teams.router)
app.include_router(submisions.router)