def generate_verification_report(document_type: str, extracted_data: dict) -> dict:
    """
    Analyzes the extracted data to check for missing fields and calculates a completeness score.
    """
    report = {
        "completeness_score": 0,
        "verification_status": "Pending",
        "missing_fields": [],
        "recommended_action": "None"
    }

    # If the document is unknown, we can't verify it
    if document_type == "Unknown/Unclassified":
        report["verification_status"] = "Manual Review Required"
        report["recommended_action"] = "Please upload a valid CNIC, Resume, or Transcript."
        return report

    # 1. Define the required fields for each document type
    # 1. Define the required fields for each document type
    required_fields = []
    if document_type == "CNIC":
        required_fields = ["identity_number", "date_of_birth", "date_of_issue", "date_of_expiry"]
    elif document_type == "Resume":
        # Added LinkedIn and GitHub to the required verification checklist
        required_fields = ["emails", "phone_numbers", "linkedin_urls", "github_urls"]
    # 2. Check which fields are missing or empty
    present_fields = 0
    for field in required_fields:
        value = extracted_data.get(field)
        # Check if the value exists and is not empty (handles strings and lists)
        if value and len(value) > 0:
            present_fields += 1
        else:
            report["missing_fields"].append(field)

    # 3. Calculate Completeness Score (0 to 100)
    if required_fields:
        score = int((present_fields / len(required_fields)) * 100)
        report["completeness_score"] = score

    # 4. Determine Status & Actions based on the score
    if report["completeness_score"] == 100:
        report["verification_status"] = "Verified"
        report["recommended_action"] = "Proceed to automated approval pipeline."
    elif report["completeness_score"] >= 50:
        report["verification_status"] = "Partially Verified"
        report["recommended_action"] = "Flagged for human review. Missing partial data."
    else:
        report["verification_status"] = "Rejected"
        report["recommended_action"] = "Request user to re-upload a clearer document."

    return report