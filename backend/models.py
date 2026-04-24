from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

'''
This file defines SQLAlchemy models that map to database tables.
These models represent the structure of the database and relationships between entities.
'''

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Foreign Key → Division
    div_id = Column(String, ForeignKey("divisions.id"), nullable=False)

    # Relationships
    division = relationship("Division", back_populates="participants")
    allocations = relationship("Allocation", back_populates="participant")


class Division(Base):
    __tablename__ = "divisions"

    # Using 'A', 'B', 'C' as IDs
    id = Column(String, primary_key=True)

    total_participants = Column(Integer, nullable=False)
    seats_allo = Column(Integer, nullable=False)
    max_per_sess = Column(Integer, nullable=False)

    # Relationships
    participants = relationship("Participant", back_populates="division")


class Session(Base):
    __tablename__ = "sessions"

    # 'morning', 'midday', 'afternoon'
    id = Column(String, primary_key=True)

    time_slot = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)  # Should be 20
    duration = Column(Integer, nullable=False)  #  90 minutes

    # Relationships
    allocations = relationship("Allocation", back_populates="session")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # store hashed password


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    part_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    sess_id = Column(String, ForeignKey("sessions.id"), nullable=False)

    # Constraint: participant can only be assigned once
    __table_args__ = (
        UniqueConstraint('part_id', name='unique_participant_allocation'),
    )

    # Relationships
    participant = relationship("Participant", back_populates="allocations")
    session = relationship("Session", back_populates="allocations")