import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .user import User


class AppointmentStatus(enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELED = "canceled"
    IN_PROGRESS = "in_progress"


class Appointment(Base):
    __tablename__ = "appointment"

    id: Mapped[int] = mapped_column(primary_key=True)

    # ForeignKey to the User model for patient and doctor
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id"), nullable=False
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id"), nullable=False
    )

    # Relationships to the User model
    patient: Mapped["User"] = relationship(
        back_populates="patient_appointments", foreign_keys=[patient_id]
    )
    doctor: Mapped["User"] = relationship(
        back_populates="doctor_appointments", foreign_keys=[doctor_id]
    )

    # Scheduled start and end times
    appointment_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    appointment_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Appointment status using the AppointmentStatus enum
    status: Mapped[AppointmentStatus] = mapped_column(
        SQLAlchemyEnum(
            AppointmentStatus,
            native_enum=True,  # Use DB-native enum if supported
            length=15,  # For databases without enum support
            validate_strings=True,
        ),
        nullable=False,
        default=AppointmentStatus.SCHEDULED,
    )
