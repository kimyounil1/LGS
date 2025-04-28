from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from LGS.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    personas = relationship("AIPersona", back_populates="owner")
