import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import cv2
import numpy as np

# Point pytesseract to the Tesseract executable on Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
    
    # Returning the grayscale image directly. 
    # For CNICs, keeping the contrast natural often works better than forcing black/white.
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
            
            # config='--psm 6' tells Tesseract to assume a single uniform block of text.
            # config='--psm 11' (sparse text) is also great for scattered ID fields.
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