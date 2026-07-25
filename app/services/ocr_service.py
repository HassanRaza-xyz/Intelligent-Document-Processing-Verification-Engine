import os
import platform 
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import cv2
import numpy as np

# Dynamically set Tesseract path ONLY if running on Windows
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# If on Linux (Docker), pytesseract will automatically find it in the system PATH.

def preprocess_image(image_path: str) -> Image.Image:
    """
    Refined preprocessing for complex backgrounds like CNICs.
    Scales the image up and converts to grayscale without aggressive thresholding.
    """
    img = cv2.imread(image_path)
    
    # 1. Scale image up by 2x. Tesseract reads larger text much better.
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # 2. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    return Image.fromarray(gray)

def extract_text_from_file(file_path: str) -> str:
    """
    Detects the file type, preprocesses if necessary, and extracts text.
    """
    ext = os.path.splitext(file_path)[1].lower()
    extracted_text = ""

    try:
        if ext in ['.png', '.jpg', '.jpeg']:
            processed_image = preprocess_image(file_path)
            custom_config = r'--oem 3 --psm 11' 
            extracted_text = pytesseract.image_to_string(processed_image, config=custom_config)
        
        elif ext == '.pdf':
            doc = fitz.open(file_path)
            for page in doc:
                extracted_text += page.get_text()
            
            if not extracted_text.strip():
                extracted_text = "[Notice: Scanned PDF without text layer detected. Requires advanced PDF OCR.]"
                
    except Exception as e:
        return f"Error extracting text: {str(e)}"

    return extracted_text.strip()