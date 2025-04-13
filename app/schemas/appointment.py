from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models import AppointmentStatus


class _AppointmentBase(BaseModel):
    appointment_start: datetime
    appointment_end: datetime


class AppointmentCreate(_AppointmentBase):
    # Add any required fields for creation that aren't in base
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None


class AppointmentUpdate(_AppointmentBase):
    status: Optional[AppointmentStatus] = None


class AppointmentListItem(_AppointmentBase):
    id: int
    status: AppointmentStatus
    doctor_name: str  # Example of denormalized data
