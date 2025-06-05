from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UploadedConversationCreate(BaseModel):
    persona_id: int
    content: str
    
class UploadedConversationOut(BaseModel):
    id: int
    persona_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True