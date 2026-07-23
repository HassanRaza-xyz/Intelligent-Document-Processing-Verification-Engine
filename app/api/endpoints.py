from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from app.services.ocr_service import extract_text_from_file
from app.services.nlp_service import extract_structured_data
from app.services.classification_service import classify_document # <-- NEW IMPORT

router = APIRouter()
UPLOAD_DIR = "uploaded_docs"

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF and images are supported."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    # 1. Get raw text from OCR
    raw_text = extract_text_from_file(file_path)
    
    # 2. Classify the document type
    document_type = classify_document(raw_text)
    
    # 3. Extract structured data (We can later make this conditional based on doc type)
    structured_data = extract_structured_data(raw_text)

    # 4. Return the complete analysis
    return {
        "filename": file.filename,
        "status": "success",
        "message": "Document processed successfully",
        "document_type": document_type, # <-- NEW: Shows the classification
        "extracted_data": structured_data, 
        "raw_text": raw_text
    }