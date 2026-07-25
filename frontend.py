import streamlit as st
import requests
import json

# Set the page configuration
st.set_page_config(page_title="Ezitech AI Document Engine", layout="wide")

st.title("📄 Intelligent Document Processing Engine")
st.markdown("**Ezitech Case Study AI-004** | AI-powered extraction, classification, and verification.")

# Sidebar for configuration
st.sidebar.header("API Configuration")
api_url = st.sidebar.text_input("FastAPI URL", "http://127.0.0.1:8000/api/v1/upload/")

# Main upload widget
uploaded_file = st.file_uploader("Upload an Internship Document (PDF, JPG, PNG)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info(f"File '{uploaded_file.name}' selected. Ready for AI processing.")
    
    if st.button("Analyze Document"):
        with st.spinner("Extracting & Verifying... Please wait."):
            # Prepare the file for the POST request
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            try:
                # Call our FastAPI Backend
                response = requests.post(api_url, files=files)
                response.raise_for_status()
                data = response.json()
                
                st.success("✅ Document Processed Successfully!")
                
                # --- UI Layout ---
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Verification Report")
                    report = data.get("verification_report", {})
                    
                    # Display metrics
                    m1, m2 = st.columns(2)
                    m1.metric("Completeness Score", f"{report.get('completeness_score', 0)}%")
                    m2.metric("Confidence Score", f"{report.get('confidence_score', 0)}%")
                    
                    st.write(f"**Status:** {report.get('verification_status')}")
                    st.write(f"**Recommendation:** {report.get('recommended_action')}")
                    
                    if report.get("is_blurry"):
                        st.error("⚠️ Blurry Image Detected!")
                    if report.get("expiry_alert"):
                        st.error("🚨 Document has Expired!")
                        
                    if report.get("missing_fields"):
                        st.warning(f"Missing Fields: {', '.join(report.get('missing_fields'))}")
                
                with col2:
                    st.subheader(f"Extracted Data ({data.get('document_type', 'Unknown')})")
                    # Display the JSON cleanly
                    st.json(data.get("extracted_data", {}))
                
                st.subheader("Raw OCR Output")
                with st.expander("Click to view raw text"):
                    st.text(data.get("raw_text", ""))
                    
            except requests.exceptions.RequestException as e:
                st.error(f"API Error: Make sure your FastAPI server is running! Details: {e}")