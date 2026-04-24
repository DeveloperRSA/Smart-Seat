from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime

DivisionType = Literal["A", "B", "C"]
SessionType = Literal["morning", "midday", "afternoon"]

# Participant schemas
class ParticipantBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    division: DivisionType

class ParticipantCreate(ParticipantBase):
    pass

class ParticipantResponse(ParticipantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Session schemas
class SessionBase(BaseModel):
    name: SessionType

class SessionResponse(SessionBase):
    id: int
    capacity: int  # should always be 20
    start_time: str
    end_time: str

    class Config:
        from_attributes = True

class AllocationCreate(BaseModel):
    participant_id: int
    session_id: int

class AllocationResponse(BaseModel):
    id: int
    participant_id: int
    session_id: int
    session_name: str
    division: DivisionType

    class Config:
        from_attributes = True

class AllocationResult(BaseModel):
    success: bool
    message: str

# Session availability
class SessionAvailability(BaseModel):
    session_id: int
    session_name: str
    remaining_seats: int
    remaining_division_A: int
    remaining_division_B: int
    remaining_division_C: int

