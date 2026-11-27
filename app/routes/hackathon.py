from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas,models,oauth2
from app.database import get_db

router = APIRouter(
    tags=["Hackathon"]
)   

@router.get("/hackathons", response_model=list[schemas.HackathonOut])
async def get_hackathons(db: Session = Depends(get_db),
                        current_user = Depends(oauth2.get_current_user)):
    hack_details = db.query(models.Hackathon).all()
 
    return hack_details

@router.get("/hackathons/{id}" ,response_model = schemas.HackathonOut)
async def get_one_hackathon(id:int, db:Session = Depends(get_db),
                            current_user = Depends(oauth2.get_current_user)):
    hack_detalis = db.query(models.Hackathon).filter(models.Hackathon.id == id).first()
    if not hack_detalis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = "Details of the Hackathon is not found")
    return hack_detalis

@router.post("/hackathons")
async def create_Hackathon(hack: schemas.HackathonCreate, db:Session = Depends(get_db),
                      current_user = Depends(oauth2.get_current_user)):
    new_hackathon = models.Hackathon(**hack.model_dump(), created_by = current_user.id)
    db.add(new_hackathon)
    db.commit()
    db.refresh(new_hackathon)
    return new_hackathon

@router.post("/hackathons/{id}/register", response_model = schemas.HackathonRegistration)
async def register_hackathon(id:int,db:Session = Depends(get_db),
                             current_user = Depends(oauth2.get_current_user)):
    hackathon = db.query(models.Hackathon).filter(models.Hackathon.id == id).first()
    if not hackathon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found")
    
    exisiting_user = db.query(models.Hackathon_registration).filter(
        models.Hackathon_registration.user_id == current_user.id,
        models.Hackathon_registration.hackathon_id == id
    ).first()

    if exisiting_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User is already registered in the hackathon")

    new_registration = models.Hackathon_registration(user_id=current_user.id, hackathon_id=id)
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    return new_registration
