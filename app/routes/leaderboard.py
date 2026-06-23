from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import schemas,models,oauth2
from app.database import get_db

router = APIRouter(
    tags=["leaderboard"]
) 

@router.get("/hackathons/{hackathon_id}/leaderboard",response_model= list[schemas.LeaderboardOut] )
async def leaderboard(hackathon_id : int,
                       db:Session = Depends(get_db),
                      current_user = Depends(oauth2.get_current_user)):
    
    lead = (
        db.query(
            models.Team.name,
            func.avg(models.Vote.score).label("avg_score"),
            func.count(models.Vote.user_id).label("vote_count")
        )
        .join(
            models.Submission,
            models.Submission.team_id == models.Team.id
        )
        .join(
            models.Vote,
            models.Vote.submission_id == models.Submission.id
        )
        .filter(
            models.Team.hackathon_id == hackathon_id
        )
        .group_by(
            models.Team.id,
            models.Team.name
        )
        .order_by(
            func.avg(models.Vote.score).desc()
        )
        .all()
    )

    result = []
    for rank,team in enumerate(lead, start=1):
        result.append({
        "rank": rank,
        "team_name": team.name,
        "avg_score": round(team.avg_score, 2),
        "vote_count": team.vote_count
    })

    return result