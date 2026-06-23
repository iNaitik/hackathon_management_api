from datetime import datetime
from pydantic import BaseModel, ConfigDict,EmailStr

# Users Schema
class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Login Schema
class UserLogin(BaseModel):
    email : EmailStr
    password : str

# JWT Authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int

# Hackathons
class HackathonOut(BaseModel):
    id: int
    title: str
    description: str
    created_by: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class HackathonCreate(BaseModel):
    title: str
    description: str


# Teams
class TeamCreate(BaseModel):
    name:str
    hackathon_id:int    

class TeamOut(BaseModel):
    id: int
    name: str
    hackathon_id : int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Submission
class Submission(BaseModel):
    project_name : str
    demo_link : str

class SubmissionOut(BaseModel):
    id:int
    project_name: str
    demo_link : str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Votes
class VoteCreate(BaseModel):
    score:int
    
class VoteOut(BaseModel):
    user_id: int
    submission_id: int
    score: int

    model_config = ConfigDict(from_attributes=True)

# LeaderBoard
class LeaderboardOut(BaseModel):
    team_name: str
    avg_score: float
    vote_count: int
