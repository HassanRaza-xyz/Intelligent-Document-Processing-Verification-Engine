from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from app.services.ocr_service import extract_text_from_file # Import our new service

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

    # -- NEW: Extract text using our OCR service --
    raw_text = extract_text_from_file(file_path)

    return {
        "filename": file.filename,
        "status": "success",
        "message": "Document uploaded and processed successfully",
        "saved_path": file_path,
        "extracted_text": raw_text # Return the extracted text in the response
    }