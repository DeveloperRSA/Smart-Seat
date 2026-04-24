from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Participant, Session as TrainingSession, Allocation
from backend.schemas import AllocationCreate, AllocationResult

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/participants")
def get_participants(db: Session = Depends(get_db)):
    return db.query(Participant).all()


@router.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(TrainingSession).all()


@router.get("/allocations")
def get_allocations(db: Session = Depends(get_db)):
    return db.query(Allocation).all()


@router.post("/allocate", response_model=AllocationResult)
def allocate_participant(data: AllocationCreate, db: Session = Depends(get_db)):

    participant = db.query(Participant).filter(
        Participant.id == data.participant_id
    ).first()

    if not participant:
        return AllocationResult(success=False, message="Participant not found")

    session = db.query(TrainingSession).filter(
        TrainingSession.id == data.session_id
    ).first()

    if not session:
        return AllocationResult(success=False, message="Session not found")

    existing = db.query(Allocation).filter(
        Allocation.part_id == data.participant_id
    ).first()

    if existing:
        return AllocationResult(success=False, message="Already allocated")

    session_count = db.query(Allocation).filter(
        Allocation.sess_id == data.session_id
    ).count()

    if session_count >= session.capacity:
        return AllocationResult(success=False, message="Session full")

    allocation = Allocation(
        part_id=data.participant_id,
        sess_id=data.session_id
    )

    db.add(allocation)
    db.commit()

    return AllocationResult(success=True, message="Allocated successfully")