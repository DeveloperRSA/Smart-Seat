from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Session

from backend.database import Base, engine, SessionLocal
from backend.models import Participant, Division, Session as TrainingSession, Allocation

'''
SQLAlchemy models + seed script for Smart Seat Allocation system
'''


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    div_id = Column(String, ForeignKey("divisions.id"), nullable=False)

    division = relationship("Division", back_populates="participants")
    allocations = relationship("Allocation", back_populates="participant")


class Division(Base):
    __tablename__ = "divisions"

    id = Column(String, primary_key=True)

    total_participants = Column(Integer, nullable=False)
    seats_allo = Column(Integer, nullable=False)
    max_per_sess = Column(Integer, nullable=False)

    participants = relationship("Participant", back_populates="division")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)

    time_slot = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)

    allocations = relationship("Allocation", back_populates="session")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)

    part_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    sess_id = Column(String, ForeignKey("sessions.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('part_id', name='unique_participant_allocation'),
    )

    participant = relationship("Participant", back_populates="allocations")
    session = relationship("Session", back_populates="allocations")




def seed_database(db: Session):


    if db.query(Division).count() == 0:
        divisions = [
            Division(id="A", total_participants=24, seats_allo=0, max_per_sess=8),
            Division(id="B", total_participants=18, seats_allo=0, max_per_sess=6),
            Division(id="C", total_participants=18, seats_allo=0, max_per_sess=6),
        ]
        db.add_all(divisions)
        db.commit()


    if db.query(Session).count() == 0:
        sessions = [
            Session(id="morning", time_slot="09:00-10:30", capacity=20, duration=90),
            Session(id="midday", time_slot="11:00-12:30", capacity=20, duration=90),
            Session(id="afternoon", time_slot="13:00-14:30", capacity=20, duration=90),
        ]
        db.add_all(sessions)
        db.commit()


    if db.query(Participant).count() == 0:

        divisions_config = {"A": 24, "B": 18, "C": 18}

        first_names = ["James", "Mary", "Robert", "Patricia", "John"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]

        participants = []
        i = 0

        for div_id, count in divisions_config.items():
            for _ in range(count):

                name = first_names[i % len(first_names)]
                surname = last_names[i % len(last_names)]

                email = f"{name.lower()}.{surname.lower()}{i}@example.com"

                participants.append(
                    Participant(
                        name=name,
                        surname=surname,
                        email=email,
                        div_id=div_id
                    )
                )
                i += 1

        db.add_all(participants)
        db.commit()


if __name__ == "__main__":

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_database(db)
        print("Database seeded successfully")
    except Exception as e:
        db.rollback()
        print("Error:", e)
    finally:
        db.close()