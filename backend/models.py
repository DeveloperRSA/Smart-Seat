from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

'''
This file defines SQLAlchemy models that map to database tables.
These models represent the structure of the database and relationships between entities.
'''

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)

    # Foreign Keys
    div_id = Column(String, ForeignKey("divisions.id"))
    sess_id = Column(String, ForeignKey("sessions.id"), nullable=True)

    # Relationships
    division = relationship("Division", back_populates="participants")
    session = relationship("Session", back_populates="participants")
    allocations = relationship("Allocation", back_populates="participant")


class Division(Base):
    __tablename__ = "divisions"

    id = Column(String, primary_key=True)  # 'A', 'B', or 'C'
    total_participants = Column(Integer, nullable=False)
    seats_allo = Column(Integer, nullable=False)
    max_per_sess = Column(Integer, nullable=False)

    # Relationships
    participants = relationship("Participant", back_populates="division")
    allocations = relationship("Allocation", back_populates="division")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    time_slot = Column(String)
    capacity = Column(Integer)
    assigned_seats = Column(Integer, default=0)
    duration = Column(Integer)  # In minutes

    # Relationships
    participants = relationship("Participant", back_populates="session")
    allocations = relationship("Allocation", back_populates="session")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # This will store the hashed password


class Allocation(Base):
    __tablename__ = "allocations"

    # Composite primary key or individual PK
    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, ForeignKey("participants.id"))
    div_id = Column(String, ForeignKey("divisions.id"))
    sess_id = Column(String, ForeignKey("sessions.id"))

    # Relationships for easy access
    participant = relationship("Participant", back_populates="allocations")
    division = relationship("Division", back_populates="allocations")
    session = relationship("Session", back_populates="allocations")
>>>>>>> Stashed changes
