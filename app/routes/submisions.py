from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas,models,oauth2
from app.database import get_db

router = APIRouter(
    tags = ["Submission"]
)

@router.post("/teams/{teams_id}/submit",response_model=schemas.SubmissionOut,
    status_code=status.HTTP_201_CREATED)
async def submit(teams_id: int, team_submision: schemas.Submission, 
                 db:Session = Depends(get_db),
                 current_user = Depends(oauth2.get_current_user)):
    team = db.query(models.Team).filter(models.Team.id == teams_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Team not found")
    team_member = db.query(models.Team_Member).filter(
        models.Team_Member.user_id == current_user.id,
        models.Team_Member.team_id == teams_id
    ).first()
    
    if not team_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are not member of a team")
    
    existing_submission = db.query(models.Submission).filter(
        models.Submission.team_id == teams_id).first()
    
    if existing_submission:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Team has already submitted")
    new_submission = models.Submission(**team_submision.model_dump(),team_id = teams_id)
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return new_submission