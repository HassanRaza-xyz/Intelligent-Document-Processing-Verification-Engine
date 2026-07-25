# Intelligent Document Processing & Verification Engine

**Ezitech Engineering Framework (EEF) | Industry AI Case Study – AI-004**

## Project Overview
This project is an AI-powered Intelligent Document Processing Engine built for the Ezitech Internship Portal. It automates the verification of submitted documents (Resumes, CNICs, Transcripts) by reading the files, classifying the document type, extracting structured information, and generating a verification completeness score to reduce manual administrative effort.

## Core Features
*   **Document Classification:** Automatically identifies Resumes, CNICs, and Transcripts using NLP keywords.
*   **OCR Pipeline:** Extracts raw text from images and PDFs using **Tesseract OCR** and **PyMuPDF**.
*   **Image Preprocessing:** Utilizes **OpenCV** to scale and convert complex documents (like CNICs) to grayscale for high-accuracy extraction.
*   **Information Extraction:** Robust Regular Expressions (Regex) parse unstructured text into clean JSON (fetching IDs, DOBs, Emails, Phone Numbers, GitHub, and LinkedIn URLs).
*   **Rule-Based Verification:** Evaluates extracted data against required fields to generate a Completeness Score (0-100%) and actionable recommendations.

## Tech Stack
*   **Backend:** Python, FastAPI, Uvicorn
*   **Computer Vision & OCR:** OpenCV, Tesseract OCR, Pillow
*   **Document Handling:** PyMuPDF (fitz), python-multipart
*   **NLP & Extraction:** Python `re` (Regular Expressions)

## Local Setup & Installation

**1. Clone the repository**
\`\`\`bash
git clone https://github.com/HassanRaza-xyz/intelligent-document-processing.git
cd intelligent-document-processing
\`\`\`

**2. Set up the virtual environment**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate
\`\`\`

**3. Install Dependencies**
Ensure you have [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed on your system.
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**4. Run the API Server**
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

## API Endpoints
*   `GET /`: Root welcome message.
*   `GET /health`: Health check endpoint.
*   `POST /api/v1/upload/`: Main endpoint accepting PDF/Image uploads. Returns a JSON response containing the document classification, raw OCR text, structured extracted data, and a verification report.

*Detailed API documentation is auto-generated at `/docs` (Swagger UI) and `/redoc`.*