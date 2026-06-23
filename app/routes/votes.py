from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas,models,oauth2
from app.database import get_db

router = APIRouter(
    tags=["Votes"]
)

@router.post("/submissions/{submission_id}/vote",response_model=schemas.VoteOut,
        status_code=status.HTTP_201_CREATED)

async def vote(submission_id: int,votes:schemas.VoteCreate,
               db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    submission = db.query(models.Submission).filter(
        models.Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Submission Does Not Exists")
    
    existing_vote = db.query(models.Vote).filter(
    models.Vote.user_id == current_user.id,
    models.Vote.submission_id == submission_id).first()

    if existing_vote:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You Have Already Voted")
    
    if votes.score < 1 or votes.score > 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Vote between 1 to 10")
    

    team_member = db.query(models.Team_Member).filter(
        models.Team_Member.team_id == submission.team_id,
        models.Team_Member.user_id == current_user.id).first()
    
    if team_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot vote for your own team")
    
    vote = models.Vote(
        user_id=current_user.id,
        submission_id=submission_id,
        score=votes.score)
    
    db.add(vote)
    db.commit()
    db.refresh(vote)

    return vote
