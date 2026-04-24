from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base, SessionLocal
import backend.models
from backend.models import Participant, Division, Session as TrainingSession

from backend.routes.admin import router as admin_router

app = FastAPI(
    title="Smart Seat Allocation Platform",
    version="1.0.0"
)

app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


# -------------------------
# AUTO POPULATE DATABASE
# -------------------------
def init_data():
    db = SessionLocal()

    try:
        if db.query(Division).count() == 0:
            db.add_all([
                Division(id="A", total_participants=24, seats_allo=0, max_per_sess=8),
                Division(id="B", total_participants=18, seats_allo=0, max_per_sess=6),
                Division(id="C", total_participants=18, seats_allo=0, max_per_sess=6),
            ])
            db.commit()

        if db.query(TrainingSession).count() == 0:
            db.add_all([
                TrainingSession(id="morning", time_slot="09:00-10:30", capacity=20, duration=90),
                TrainingSession(id="midday", time_slot="11:00-12:30", capacity=20, duration=90),
                TrainingSession(id="afternoon", time_slot="13:00-14:30", capacity=20, duration=90),
            ])
            db.commit()

        if db.query(Participant).count() == 0:

            first_names = ["James", "Mary", "Robert", "Patricia", "John"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]

            divisions = {"A": 24, "B": 18, "C": 18}

            participants = []
            i = 0

            for div, count in divisions.items():
                for _ in range(count):
                    participants.append(
                        Participant(
                            name=first_names[i % len(first_names)],
                            surname=last_names[i % len(last_names)],
                            email=f"user{i}@test.com",
                            div_id=div
                        )
                    )
                    i += 1

            db.add_all(participants)
            db.commit()

    finally:
        db.close()


init_data()


@app.get("/")
def root():
    return {"message": "Smart Seat Allocation API running"}