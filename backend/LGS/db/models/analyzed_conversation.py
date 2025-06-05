from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from LGS.db.base_class import Base

class AnalyzedConversations(Base):
    __tablename__ = 'analyzed_conversations'

    id = Column(Integer, primary_key=True, index=True)
    uploaded_conversation_id = Column(Integer, ForeignKey('uploaded_conversations.id'), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    uploaded_conversation = relationship('UploadedConversations', back_populates='analyzed_conversations')
