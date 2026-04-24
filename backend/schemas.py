from typing import Literal
from pydantic import BaseModel
from datetime import datetime

DivisionType = Literal["A", "B", "C"]
SessionType = Literal["morning", "midday", "afternoon"]

class ParticipantBase(BaseModel):
    name: str
    surname: str
    email: str
    div_id: DivisionType


class ParticipantResponse(ParticipantBase):
    id: int

    class Config:
        from_attributes = True


class DivisionResponse(BaseModel):
    id: DivisionType
    total_participants: int
    seats_allo: int
    max_per_sess: int

    class Config:
        from_attributes = True


class SessionResponse(BaseModel):
    id: SessionType
    time_slot: str
    capacity: int
    duration: int

    class Config:
        from_attributes = True


class AllocationCreate(BaseModel):
    participant_id: int
    session_id: str


class AllocationResponse(BaseModel):
    id: int
    part_id: int
    sess_id: str

    class Config:
        from_attributes = True


class AllocationResult(BaseModel):
    success: bool
    message: str


class SessionAvailability(BaseModel):
    session_id: str
    session_name: str
    remaining_seats: int
    remaining_A: int
    remaining_B: int
    remaining_C: int