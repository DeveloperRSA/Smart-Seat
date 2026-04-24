from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

'''
This file defines SQLAlchemy models that map to database tables
These models represent the structure of the database and relationships between entities
'''

# Participants table - stores participants table
class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)

    div_id = Column(Integer, ForeignKey("divisions.id"))

    division = relationship("Division", back_populates="participants")

class Division(Base):
    __tablename__ = "divisions"

    id = Column(Integer, primary_key=True)
    total_participants = Column(Integer, nullable=False)
    seats_allo = Column(Integer, nullable=False)
    max_per_sess = Column(Integer, nullable=False)

    participants = relationship("Participant", back_populates="division")


