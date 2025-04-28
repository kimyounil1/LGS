from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    persona_id: int
    sender: str  # 'user'
    content: str

class MessageOut(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
