from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, exists, or_, select

from app.db.session import DBSessionDep
from app.models import Appointment
from app.models.user import User, UserRole
from app.schemas import AppointmentCreate, AppointmentListItem
from app.services.user import get_current_user

router = APIRouter(prefix="/api/v1/appointments", tags=["appointment"])


@router.get("", response_model=List[AppointmentListItem])
async def get_appointments(
    session: DBSessionDep, current_user: User = Depends(get_current_user)
):
    if current_user.role == UserRole.PATIENT:
        a = session.execute(
            select(Appointment).where(Appointment.patient_id == current_user.id)
        )
    elif current_user.role == UserRole.DOCTOR:
        a = await session.execute(
            select(Appointment).where(Appointment.doctor_id == current_user.id)
        )
    else:
        a = session.execute(select(Appointment))

    return a.scalars().all()


@router.post("", response_model=AppointmentListItem)
async def create_appointments(
    session: DBSessionDep,
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_user),
):

    if current_user.role == UserRole.PATIENT and not appointment_data.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "msg": "doctor_id is required for doctors",
                }
            ],
        )
    elif current_user.role == UserRole.DOCTOR and not appointment_data.patient_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "msg": "patient_id is required for doctors",
            },
        )

    if current_user.role == UserRole.PATIENT:
        result = await session.execute(
            select(User).where(
                User.id == appointment_data.doctor_id, User.role == UserRole.DOCTOR
            )
        )
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "doctor not found",
                },
            )
        appointment_data.patient_id = current_user.id
    elif current_user.role == UserRole.DOCTOR:
        result = await session.execute(
            select(User).where(
                User.id == appointment_data.patient_id, User.role == UserRole.PATIENT
            )
        )
        patient = result.scalar_one_or_none()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "patient not found",
                },
            )

        appointment_data.doctor_id = current_user.id

    result = await session.execute(
        select(
            exists(Appointment).where(
                and_(
                    Appointment.appointment_start < appointment_data.appointment_end,
                    Appointment.appointment_end > appointment_data.appointment_start,
                    or_(
                        Appointment.doctor_id == appointment_data.doctor_id,
                        Appointment.patient_id == appointment_data.patient_id,
                    ),
                ),
            )
        )
    )

    appointment_exists = result.scalar()

    if appointment_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "appointment already exists",
            },
        )

    appointment = Appointment(**appointment_data.model_dump())

    session.add(appointment)
    await session.commit()
    await session.refresh(appointment)

    return appointment
