from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.database import Base
from datetime import datetime

class DocumentRecord(Base):
    __tablename__ = "document_records"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    document_type = Column(String)
    completeness_score = Column(Integer)
    verification_status = Column(String)
    extracted_data_summary = Column(String) # We will save a stringified summary of the JSON
    upload_time = Column(DateTime, default=datetime.utcnow)