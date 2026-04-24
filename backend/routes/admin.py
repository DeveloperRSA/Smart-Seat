from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models import Participant, Session as TrainingSession, Allocation

from backend.schemas import AllocationCreate, AllocationResult

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/participants")
def get_participants(division: str = None, db: Session = Depends(get_db)):

    query = db.query(Participant)

    if division:
        query = query.filter(Participant.div_id == division)

    participants = query.all()

    return participants


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
        return AllocationResult(
            success=False,
            message="Participant already assigned to a session"
        )

    session_count = db.query(Allocation).filter(
        Allocation.sess_id == data.session_id
    ).count()

    if session_count >= session.capacity:
        return AllocationResult(
            success=False,
            message="Session is full"
        )


    division_limits = {
        "A": 8,
        "B": 6,
        "C": 6
    }

    division_count = db.query(Allocation).join(Participant).filter(
        Allocation.sess_id == data.session_id,
        Participant.div_id == participant.div_id
    ).count()

    if division_count >= division_limits[participant.div_id]:
        return AllocationResult(
            success=False,
            message=f"Division {participant.div_id} limit reached for this session"
        )


    allocation = Allocation(
        part_id=data.participant_id,
        sess_id=data.session_id
    )

    db.add(allocation)
    db.commit()
    db.refresh(allocation)

    return AllocationResult(
        success=True,
        message="Participant successfully allocated"
    )