from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AIPersonaCreate(BaseModel):
    name: str
    mbti: Optional[str] = None

class AIPersonaOut(BaseModel):
    id: int
    name: str
    mbti: Optional[str]
    personality_summary: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
