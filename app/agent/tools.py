from app.db import SessionLocal
import datetime
from app.models import Appointment
import uuid
from langchain.tools import tool

@tool
def create_appointment(
    patient_name: str,
    patient_phone_number: str,
    appointment_time: str,
    reason: str = None
) -> str:
    """
    Book a dental appointment for a patient.

    Args:
        patient_name (str): Full name of the patient.
        patient_phone_number (str): Patient's phone number in the format '613-111-1111'.
        appointment_time (str): Desired appointment time in ISO 8601 format (e.g., '2024-05-24T09:10:00').
        reason (str, optional): Reason for the appointment (e.g., check-up, toothache). Defaults to None.

    Returns:
        str: A confirmation message indicating the appointment has been successfully booked.
    """
    print("create_appointment called by Echo!!!")

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