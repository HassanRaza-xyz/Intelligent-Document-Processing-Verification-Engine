import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def extract_structured_data(raw_text: str, document_type: str) -> dict:
    """
    Uses Gemini LLM to extract highly structured entities from messy OCR text.
    Bypasses Regex limitations to accurately fetch Names, Skills, CGPA, etc.
    """
    if not GEMINI_API_KEY:
        return {"error": "GEMINI_API_KEY is missing. Please add it to your .env file."}

    # Initialize the fast and cost-effective Flash model
    model = genai.GenerativeModel('gemini-2.5-flash')

    # 1. Define strict JSON schemas based on the document type
    if document_type == "CNIC":
        schema = '''{
            "name": "Applicant Full Name",
            "father_name": "Father's Full Name",
            "identity_number": "13-digit CNIC number (format: XXXXX-XXXXXXX-X)",
            "date_of_birth": "DD.MM.YYYY",
            "date_of_issue": "DD.MM.YYYY",
            "date_of_expiry": "DD.MM.YYYY"
        }'''
    elif document_type == "Resume":
        schema = '''{
            "name": "Applicant Full Name",
            "emails": ["List of email addresses"],
            "phone_numbers": ["List of phone numbers"],
            "linkedin_url": "LinkedIn profile URL or username",
            "github_url": "GitHub profile URL or username",
            "university": "Name of University",
            "degree": "Degree name (e.g., BS Artificial Intelligence)",
            "skills": ["List of technical and soft skills"],
            "experience_months": "Total months of experience (integer, estimate if needed)"
        }'''
    elif document_type == "Transcript":
        schema = '''{
            "name": "Student Name",
            "university": "University Name",
            "degree": "Degree Name",
            "cgpa": "Final CGPA (float number)",
            "graduation_year": "Year of graduation (YYYY)"
        }'''
    else:
        return {"notice": "No LLM schema defined for this document type yet."}

    # 2. Construct the strict prompt with guardrails
    prompt = f"""
    You are an expert AI data extraction engine for an enterprise document verification system.
    I will provide you with messy, unstructured OCR text extracted from a {document_type}.
    Your task is to extract the relevant information and return it EXACTLY in this JSON structure:
    {schema}

    Rules & Guardrails:
    1. Return ONLY valid JSON. Do not include markdown formatting, backticks (```json), intro, or outro text.
    2. If a specific field cannot be logically found in the text, return null for that field. Do not hallucinate or guess data.
    3. Clean up standard OCR typos (e.g., if you see a date like "10,11. 1987", format it strictly as "10.11.1987").

    Raw OCR Text:
    {raw_text}
    """

    try:
        # 3. Execute the LLM chain
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Strip potential markdown formatting if the LLM ignores the guardrail
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()
            
        # Parse and return the clean JSON dictionary
        extracted_json = json.loads(response_text)
        return extracted_json
        
    except json.JSONDecodeError:
        return {"error": "LLM failed to return a valid JSON structure.", "raw_llm_output": response_text}
    except Exception as e:
        return {"error": f"LLM Processing Error: {str(e)}"}