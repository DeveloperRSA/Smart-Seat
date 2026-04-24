from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from app.database import Base, engine, SessionLocal # Ensure these are correctly set up in app/database.py

# --- MODELS ---

class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    div_id = Column(String, ForeignKey("divisions.id"))
    sess_id = Column(String, ForeignKey("sessions.id"), nullable=True)

    division = relationship("Division", back_populates="participants")
    session = relationship("Session", back_populates="participants")
    allocations = relationship("Allocation", back_populates="participant")

class Division(Base):
    __tablename__ = "divisions"
    id = Column(String, primary_key=True)  # 'A', 'B', or 'C'
    total_participants = Column(Integer, nullable=False)
    seats_allo = Column(Integer, nullable=False, default=0)
    max_per_sess = Column(Integer, nullable=False)

    participants = relationship("Participant", back_populates="division")
    allocations = relationship("Allocation", back_populates="division")

# ... (Keep your Session, Admin, and Allocation models here as you had them) ...

# --- POPULATION LOGIC ---

def seed_database(db: Session):
    # STEP 1: Create the Divisions (Crucial for Foreign Keys)
    # Adjust 'max_per_sess' and 'total_participants' as needed
    if not db.query(Division).first():
        div_a = Division(id="A", total_participants=24, max_per_sess=10, seats_allo=0)
        div_b = Division(id="B", total_participants=18, max_per_sess=10, seats_allo=0)
        div_c = Division(id="C", total_participants=18, max_per_sess=10, seats_allo=0)
        db.add_all([div_a, div_b, div_c])
        db.commit()
        print("Divisions A, B, and C created.")

    #Generate Participants
    divisions_config = {"A": 24, "B": 18, "C": 18}
    first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael",
                    "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", 
                    "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen", "Charles",
                      "Lisa", "Daniel", "Nancy", "Matthew", "Betty", "Anthony", "Margaret",
                        "Mark", "Sandra", "Donald", "Ashley", "Steven", "Kimberly", "Paul",
                          "Emily", "Andrew", "Donna", "Joshua", "Michelle", "Kenneth",
                            "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Edward", "Deborah", "Ronald", "Stephanie",
                              "Timothy", "Rebecca", "Jason", "Sharon", "Jeffrey", "Laura", "Ryan", "Cynthia"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
                   "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
                     "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                       "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
                         "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
                           "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
                             "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", 
                             "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", 
                             "Collins", "Reyes"]

    participants_to_add = []
    current_index = 0

    for div_id, count in divisions_config.items():
        for _ in range(count):
            name = first_names[current_index]
            surname = last_names[current_index]
            email = f"{name.lower()}.{surname.lower()}{current_index}@example.com"

            new_participant = Participant(
                name=name,
                surname=surname,
                email=email,
                div_id=div_id
            )
            participants_to_add.append(new_participant)
            current_index += 1

    try:
        db.add_all(participants_to_add)
        db.commit()
        print(f"Successfully added {len(participants_to_add)} participants.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")



if __name__ == "__main__":
    
    Base.metadata.create_all(bind=engine)
    
   
    with SessionLocal() as session:
        seed_database(session)