def classify_document(raw_text: str) -> str:
    """
    Classifies the document type based on NLP keyword analysis of the OCR text.
    """
    text_lower = raw_text.lower()
    
    # Define keyword signatures for different document types
    cnic_keywords = ["national identity card", "islamic republic of pakistan", "identity number"]
    resume_keywords = ["curriculum vitae", "resume", "experience", "education", "skills"]
    transcript_keywords = ["transcript", "cgpa", "academic record", "semester"]
    
    # Check for matches
    if any(keyword in text_lower for keyword in cnic_keywords):
        return "CNIC"
    
    elif sum(keyword in text_lower for keyword in resume_keywords) >= 2:
        # Require at least 2 resume keywords to avoid false positives
        return "Resume"
        
    elif any(keyword in text_lower for keyword in transcript_keywords):
        return "Transcript"
        
    return "Unknown/Unclassified"