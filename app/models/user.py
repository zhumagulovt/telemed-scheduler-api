import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .appointment import Appointment


class UserRole(enum.Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)

    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    patronym: Mapped[str] = mapped_column(String(30), nullable=True)

    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(
            UserRole,
            native_enum=True,  # Use DB-native enum if supported
            length=10,  # For databases without enum support
            validate_strings=True,
        ),
        nullable=False,
        default=UserRole.PATIENT,
    )

    phone_number: Mapped[str] = mapped_column(
        String(15), nullable=False, unique=True, index=True
    )

    # Relationships for appointments
    patient_appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patient",
        foreign_keys="Appointment.patient_id",
    )
    doctor_appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="doctor",
        foreign_keys="Appointment.doctor_id",
    )
