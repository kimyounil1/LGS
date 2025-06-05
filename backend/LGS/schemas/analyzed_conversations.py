from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnalyzedConversationsBase(BaseModel):
    uploaded_conversation_id: int
    query: str
    response: str

class AnalyzedConversationsCreate(AnalyzedConversationsBase):
    pass

class AnalyzedConversationsOut(AnalyzedConversationsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True