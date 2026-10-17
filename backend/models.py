from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from database import Base


class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    text = Column(Text)
    skills = Column(Text)
    education = Column(String(50))
    years = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    company = Column(String(100))
    text = Column(Text)
    skills = Column(Text)
    education = Column(String(50))
    years = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)


class MatchRecord(Base):
    __tablename__ = "match_records"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer)
    job_id = Column(Integer)
    score = Column(Float)
    level = Column(String(20))
    skill_score = Column(Float)
    text_score = Column(Float)
    edu_score = Column(Float)
    years_score = Column(Float)
    matched_skills = Column(Text)
    missing_skills = Column(Text)
    suggestion = Column(Text)
    created_at = Column(DateTime, default=datetime.now)