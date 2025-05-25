from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_name = Column(String, nullable=False)
    patient_phone_number = Column(String, nullable=False)
    appointment_time = Column(DateTime, nullable=False)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

