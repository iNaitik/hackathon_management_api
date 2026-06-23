from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas,models,oauth2
from app.database import get_db

router = APIRouter(
    tags = ["Teams"]
)

@router.post("/teams",response_model=schemas.TeamOut,status_code=status.HTTP_201_CREATED)
async def create_team(team:schemas.TeamCreate, db: Session = Depends(get_db),
                      current_user = Depends(oauth2.get_current_user)):
    team_info = db.query(models.Team).join(models.Team_Member).filter(
                models.Team_Member.user_id == current_user.id, 
                models.Team.hackathon_id == team.hackathon_id).first()
    if team_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User is already in a team")
    hackathon = db.query(models.Hackathon).filter(models.Hackathon.id == team.hackathon_id).first()
    if not hackathon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This Hackathon doesnot exists")
    new_team = models.Team(**team.model_dump())
    db.add(new_team)
    db.flush()
    member = models.Team_Member(user_id = current_user.id,
                                team_id = new_team.id)
    db.add(member)
    models.Team.capacity += 1
    db.commit()
    db.refresh(new_team)

    return new_team

@router.post("/teams/{id}/join")
async def jointeam(id:int, db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    
    team = db.query(models.Team).filter(models.Team.id == id).first()
    if not team:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail="Team does not exists")
    
    existing_team = db.query(models.Team).join(models.Team_Member).filter(
                models.Team_Member.user_id == current_user.id, 
                models.Team.hackathon_id == team.hackathon_id).first()
    if existing_team:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User is already in a team")
    
    if team.capacity >= 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Team is Full")
    
    member = models.Team_Member(user_id = current_user.id,
                            team_id = team.id)
    db.add(member)
    team.capacity += 1
    db.commit()
    db.refresh(team)

    return {"message":"Joined the team sucessfully",
            "team_id": team.id}

    