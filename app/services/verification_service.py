import cv2
from datetime import datetime

def check_image_blur(file_path: str, threshold: float = 100.0) -> bool:
    """Uses OpenCV to calculate the variance of the Laplacian to detect blur."""
    img = cv2.imread(file_path)
    if img is None: 
        return False # Not an image (likely a PDF)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < threshold

def generate_verification_report(document_type: str, extracted_data: dict, file_path: str) -> dict:
    report = {
        "completeness_score": 0,
        "confidence_score": 85.5, # Default baseline confidence
        "verification_status": "Pending",
        "missing_fields": [],
        "recommended_action": "None",
        "expiry_alert": False,
        "is_blurry": False
    }

    # --- NEW: Check for blurriness ---
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        if check_image_blur(file_path):
            report["is_blurry"] = True
            report["confidence_score"] -= 30.0 # Drop confidence if blurry

    if document_type == "Unknown/Unclassified":
        report["verification_status"] = "Manual Review Required"
        report["recommended_action"] = "Please upload a valid CNIC, Resume, or Transcript."
        report["confidence_score"] = 10.0
        return report

    required_fields = []
    if document_type == "CNIC":
        required_fields = ["identity_number", "date_of_birth", "date_of_issue", "date_of_expiry"]
        expiry_str = extracted_data.get("date_of_expiry")
        if expiry_str:
            try:
                expiry_date = datetime.strptime(expiry_str, "%d.%m.%Y")
                if expiry_date < datetime.now():
                    report["expiry_alert"] = True
            except ValueError:
                pass 

    elif document_type == "Resume":
        required_fields = ["emails", "phone_numbers", "linkedin_urls", "github_urls"]

    present_fields = 0
    for field in required_fields:
        value = extracted_data.get(field)
        if value and len(value) > 0:
            present_fields += 1
        else:
            report["missing_fields"].append(field)

    if required_fields:
        report["completeness_score"] = int((present_fields / len(required_fields)) * 100)
        # Adjust confidence based on completeness
        report["confidence_score"] = min(99.9, report["confidence_score"] * (report["completeness_score"] / 100 + 0.2))

    if report["is_blurry"]:
        report["verification_status"] = "Rejected (Blurry Image)"
        report["recommended_action"] = "Image is too blurry. Please re-upload a high-quality scan."
    elif report["expiry_alert"]:
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

    # Round confidence score for clean output
    report["confidence_score"] = round(report["confidence_score"], 2)

    return report