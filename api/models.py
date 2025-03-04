from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Conversation(Base):
    __tablename__ = "application_logs"
    id =  Column(Integer, primary_key=True, index=True)
    session_id =  Column(String, unique=True)
    created_at =  Column(TIMESTAMP, default=datetime.now())

    messages = relationship("Messages", back_populates="messages")

class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("application_logs"))
    user_query = Column(String)
    ai_response = Column(String)

    messages = relationship("Conversation", back_populates="messages")

