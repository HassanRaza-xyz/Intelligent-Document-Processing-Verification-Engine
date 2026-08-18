from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
import shutil
import json
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import DocumentRecord

from app.services.ocr_service import extract_text_from_file
from app.services.nlp_service import extract_structured_data
from app.services.classification_service import classify_document
from app.services.verification_service import generate_verification_report

router = APIRouter()
UPLOAD_DIR = "uploaded_docs"

@router.post("/upload/")
async def upload_document(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # 1. File Type Validation
    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF and images are supported."
        )

    # --- NEW: Step 2 - Duplicate Upload Detection ---
    # Database mein check karein ke kya yeh file pehle se maujood hai
    existing_document = db.query(DocumentRecord).filter(DocumentRecord.filename == file.filename).first()
    
    if existing_document:
        raise HTTPException(
            status_code=409, # HTTP 409 Conflict status for duplicates
            detail=f"Duplicate Upload Detected: '{file.filename}' has already been processed and verified."
        )
    # ------------------------------------------------

    # 2. Save the file locally
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    # 3. AI Pipeline Execution
    raw_text = extract_text_from_file(file_path)
    document_type = classify_document(raw_text)
    structured_data = extract_structured_data(raw_text, document_type)
    
    # Pass file_path for blur detection
    verification_report = generate_verification_report(document_type, structured_data, file_path)

    # 4. Save New Record to Database
    db_record = DocumentRecord(
        filename=file.filename,
        document_type=document_type,
        completeness_score=verification_report["completeness_score"],
        verification_status=verification_report["verification_status"],
        extracted_data_summary=json.dumps(structured_data) 
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return {
        "record_id": db_record.id, 
        "filename": file.filename,
        "status": "success",
        "message": "Document processed and saved to database successfully",
        "document_type": document_type,
        "verification_report": verification_report,
        "extracted_data": structured_data, 
        "raw_text": raw_text
    }

@router.get("/documents/")
async def get_all_documents(db: Session = Depends(get_db)):
    """
    Retrieves all processed document records from the database.
    """
    records = db.query(DocumentRecord).all()
    
    for record in records:
        if record.extracted_data_summary:
            record.extracted_data_summary = json.loads(record.extracted_data_summary)
            
    return {
        "total_processed": len(records),
        "documents": records
    }   