from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from LGS.db.base_class import Base

class UploadedConversations(Base):
    __tablename__ = 'uploaded_conversations'

    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(Integer, ForeignKey('persona.id'), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_analyzed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    expiration_date = Column(DateTime, nullable=True)

    persona = relationship('Persona', back_populates='conversations')
    analyzed_conversations = relationship('AnalyzedConversations', back_populates='uploaded_conversation')
    deleted_conversations = relationship('DeletedConversations', back_populates='uploaded_conversation')