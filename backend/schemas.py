from pydantic import BaseModel, Field


class ResumeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=10, max_length=5000)


class JobCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    company: str = ""
    text: str = Field(..., min_length=10, max_length=5000)


class MatchRequest(BaseModel):
    resume_id: int
    job_id: int


class BatchMatchRequest(BaseModel):
    resume_id: int