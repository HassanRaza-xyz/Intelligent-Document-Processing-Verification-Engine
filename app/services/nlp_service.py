import re

def extract_cnic_data(raw_text: str) -> dict:
    """Extracts identity numbers and dates from a CNIC."""
    extracted_data = {
        "identity_number": None,
        "date_of_birth": None,
        "date_of_issue": None,
        "date_of_expiry": None
    }

    cnic_pattern = r'\b\d{5}-?\d{7}-?\d{1}\b'
    cnic_match = re.search(cnic_pattern, raw_text)
    if cnic_match:
        raw_id = cnic_match.group(0).replace("-", "")
        if len(raw_id) == 13:
            extracted_data["identity_number"] = f"{raw_id[:5]}-{raw_id[5:12]}-{raw_id[12:]}"

    date_pattern = r'\b\d{2}[.,\-\s]+\d{2}[.,\-\s]+\d{4}\b'
    raw_dates = re.findall(date_pattern, raw_text)
    
    clean_dates = [re.sub(r'[.,\-\s]+', '.', d) for d in raw_dates]
    
    if len(clean_dates) >= 1: extracted_data["date_of_birth"] = clean_dates[0]
    if len(clean_dates) >= 2: extracted_data["date_of_issue"] = clean_dates[1]
    if len(clean_dates) >= 3: extracted_data["date_of_expiry"] = clean_dates[2]

    return extracted_data


def extract_resume_data(raw_text: str) -> dict:
    """Extracts contact information, professional links, and basic entities from a Resume."""
    extracted_data = {
        "emails": [],
        "phone_numbers": [],
        "linkedin_urls": [],
        "github_urls": []
    }
    
    # 1. Regex for Email Addresses
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    extracted_data["emails"] = list(set(re.findall(email_pattern, raw_text)))
    
    # 2. Regex for Phone Numbers 
    phone_pattern = r'(?:\+?92[\s\-]?|0)?3\d{2}[\s\-]?\d{7}'
    extracted_data["phone_numbers"] = list(set(re.findall(phone_pattern, raw_text)))
    
    # 3. Regex for LinkedIn Profiles
    linkedin_pattern = r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+'
    extracted_data["linkedin_urls"] = list(set(re.findall(linkedin_pattern, raw_text)))

    # 4. Regex for GitHub Profiles
    github_pattern = r'(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+'
    extracted_data["github_urls"] = list(set(re.findall(github_pattern, raw_text)))
    
    return extracted_data


def extract_structured_data(raw_text: str, document_type: str) -> dict:
    """
    Acts as a router to call the correct extraction logic based on document type.
    """
    if document_type == "CNIC":
        return extract_cnic_data(raw_text)
    elif document_type == "Resume":
        return extract_resume_data(raw_text)
    else:
        return {"notice": "Structured extraction for this document type is not yet defined."}