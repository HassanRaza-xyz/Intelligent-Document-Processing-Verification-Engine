import re

def extract_structured_data(raw_text: str) -> dict:
    """
    Parses raw OCR text to extract structured entities using robust Regular Expressions.
    """
    extracted_data = {
        "identity_number": None,
        "date_of_birth": None,
        "date_of_issue": None,
        "date_of_expiry": None
    }

    # 1. Regex Pattern for Pakistani CNIC
    cnic_pattern = r'\b\d{5}-?\d{7}-?\d{1}\b'
    cnic_match = re.search(cnic_pattern, raw_text)
    
    if cnic_match:
        raw_id = cnic_match.group(0).replace("-", "")
        if len(raw_id) == 13:
            extracted_data["identity_number"] = f"{raw_id[:5]}-{raw_id[5:12]}-{raw_id[12:]}"

    # 2. Robust Regex Pattern for Dates 
    # Accounts for OCR errors like: 12.06.2013, 10,11. 1987, 12-06-2020, 10 11 1987
    date_pattern = r'\b\d{2}[.,\-\s]+\d{2}[.,\-\s]+\d{4}\b'
    raw_dates = re.findall(date_pattern, raw_text)
    
    # 3. Clean and standardize the extracted dates
    clean_dates = []
    for d in raw_dates:
        # Replace any sequence of punctuation or spaces with a single dot
        clean_date = re.sub(r'[.,\-\s]+', '.', d)
        clean_dates.append(clean_date)
    
    # Assign the cleaned dates based on standard CNIC layout order
    if len(clean_dates) >= 1:
        extracted_data["date_of_birth"] = clean_dates[0]
    if len(clean_dates) >= 2:
        extracted_data["date_of_issue"] = clean_dates[1]
    if len(clean_dates) >= 3:
        extracted_data["date_of_expiry"] = clean_dates[2]

    return extracted_data