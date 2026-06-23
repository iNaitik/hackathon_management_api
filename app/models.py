from app.database import Base
from sqlalchemy import TIMESTAMP, CheckConstraint, Column, ForeignKey,Integer,String,text

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String ,nullable=False)
    description = Column(String,nullable=True)
    created_by = Column (Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String ,nullable=False)
    hackathon_id = Column(Integer,ForeignKey("hackathons.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    capacity = Column(Integer, nullable=False, default=1)
class Team_Member(Base):
    __tablename__ = "team_members"
    
    user_id = Column(Integer,ForeignKey("users.id",ondelete = "CASCADE"),primary_key=True)
    team_id = Column(Integer,ForeignKey("teams.id",ondelete = "CASCADE"),primary_key=True)
    joined_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer,primary_key=True, nullable=False)
    team_id = Column(Integer,ForeignKey("teams.id",ondelete="CASCADE"),nullable=False,unique=True)
    project_name = Column(String,nullable=False)
    demo_link = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,ForeignKey("users.id",ondelete = "CASCADE"),primary_key=True)
    submission_id = Column(Integer,ForeignKey("submissions.id",ondelete="CASCADE"),primary_key=True)
    score = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("score >= 1 AND score <= 10", name="score_range"),
    )






