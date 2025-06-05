from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from LGS.db.base_class import Base

class DeletedConversations(Base):
    __tablename__ = 'deleted_conversations'

    id = Column(Integer, primary_key=True, index=True)
    uploaded_conversation_id = Column(Integer, ForeignKey('uploaded_conversations.id'), nullable=False)
    deleted_at = Column(DateTime, default=datetime.utcnow)
    reason = Column(String(255), nullable=True)

    uploaded_conversation = relationship('UploadedConversations')