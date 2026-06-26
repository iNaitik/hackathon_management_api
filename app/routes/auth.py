from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas,utils,models,oauth2
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    tags = ["Authentication"]
)

@router.post('/register',response_model=schemas.UserOut)
async def register(user:schemas.UserCreate, db: Session = Depends(get_db) ):
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post('/login',response_model=schemas.Token)
async def login(user:schemas.UserLogin, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    if not utils.verify(user.password,db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Invalid Credentials") 
    
    access_token = oauth2.create_access_token(data={"user_id":db_user.id})

    return {
        "access_token":access_token,
        "token_type": "bearer"
    }

@router.get("/")
async def me():
    return "Welcome Buddy"