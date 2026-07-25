from datetime import datetime

def generate_verification_report(document_type: str, extracted_data: dict) -> dict:
    """
    Analyzes data for missing fields, calculates completeness, and checks expiry.
    """
    report = {
        "completeness_score": 0,
        "verification_status": "Pending",
        "missing_fields": [],
        "recommended_action": "None",
        "expiry_alert": False # <-- NEW FIELD
    }

    if document_type == "Unknown/Unclassified":
        report["verification_status"] = "Manual Review Required"
        report["recommended_action"] = "Please upload a valid CNIC, Resume, or Transcript."
        return report

    required_fields = []
    if document_type == "CNIC":
        required_fields = ["identity_number", "date_of_birth", "date_of_issue", "date_of_expiry"]
        
        # --- NEW: Bonus Challenge - Expiry Check ---
        expiry_str = extracted_data.get("date_of_expiry")
        if expiry_str:
            try:
                # Convert the extracted string (DD.MM.YYYY) into a real Python date object
                expiry_date = datetime.strptime(expiry_str, "%d.%m.%Y")
                # Compare it to right now
                if expiry_date < datetime.now():
                    report["expiry_alert"] = True
            except ValueError:
                pass # Skip if the OCR read the date incorrectly and it can't be parsed

    elif document_type == "Resume":
        required_fields = ["emails", "phone_numbers", "linkedin_urls", "github_urls"]

    # Check missing fields
    present_fields = 0
    for field in required_fields:
        value = extracted_data.get(field)
        if value and len(value) > 0:
            present_fields += 1
        else:
            report["missing_fields"].append(field)

    # Calculate Score
    if required_fields:
        report["completeness_score"] = int((present_fields / len(required_fields)) * 100)

    # Determine Status & Actions
    if report["expiry_alert"]:
        # Overwrite standard status if the document is expired!
        report["verification_status"] = "Rejected (Expired Document)"
        report["recommended_action"] = "Do not proceed. Request an updated, valid CNIC."
    elif report["completeness_score"] == 100:
        report["verification_status"] = "Verified"
        report["recommended_action"] = "Proceed to automated approval pipeline."
    elif report["completeness_score"] >= 50:
        report["verification_status"] = "Partially Verified"
        report["recommended_action"] = "Flagged for human review. Missing partial data."
    else:
        report["verification_status"] = "Rejected"
        report["recommended_action"] = "Request user to re-upload a clearer document."

    return report