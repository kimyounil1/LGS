from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from LGS.db.base_class import Base

class AIPersona(Base):
    __tablename__ = "ai_personas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    mbti = Column(String, nullable=True)
    personality_summary = Column(Text, nullable=True)  # GPT로 요약한 성격
    created_at = Column(DateTime, default=datetime.utcnow)
    profile_url = Column(String, nullable=True)

    owner = relationship("User", back_populates="personas")
    messages = relationship("Message", back_populates="persona")
