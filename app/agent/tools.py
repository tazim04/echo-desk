from app.db import SessionLocal
import datetime
from app.models import Appointment
import uuid
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class AppointmentInput(BaseModel):
    patient_name: str = Field(description="Full name of the patient")
    patient_phone_number: str = Field(description="Phone number in format like 613-111-1111")
    appointment_time: str = Field(description="ISO 8601 datetime string like '2024-05-24T09:10:00'")
    reason: str = Field(default=None, description="Reason for the appointment (optional)")

def create_appointment(
    patient_name: str,
    patient_phone_number: str,
    appointment_time: str,
    reason: str = None
) -> str:
    """
    Book an appointment by providing name, phone number, ISO time string (e.g., 2024-05-24T09:10:00), and optional reason.
    """
    print("create_appointment called by Echo!!!")
    data = AppointmentInput(
        patient_name=patient_name,
        patient_phone_number=patient_phone_number,
        appointment_time=appointment_time,
        reason=reason
    )

    try:
        parsed_time = datetime.datetime.fromisoformat(appointment_time)
    except Exception as e:
        return f"Invalid time format: {e}"

    db = SessionLocal()
    try:
        appointment = Appointment(
            id=str(uuid.uuid4()),
            patient_name=patient_name,
            patient_phone_number=patient_phone_number,
            appointment_time=parsed_time,
            reason=reason
        )
        db.add(appointment)
        db.commit()
        return f"Appointment booked for {patient_name} on {parsed_time.strftime('%A, %B %d at %I:%M %p')}."
    except Exception as e:
        db.rollback()
        return f"Failed to save appointment: {e}"
    finally:
        db.close()

create_appointment_tool = StructuredTool.from_function(create_appointment)