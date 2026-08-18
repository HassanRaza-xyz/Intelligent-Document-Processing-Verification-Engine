import streamlit as st
import requests

# Set the page configuration
st.set_page_config(page_title="Ezitech AI Document Engine", layout="wide")

st.title("📄 Intelligent Document Processing Engine")
st.markdown("**Ezitech Case Study AI-004** | AI-powered extraction, classification, and verification.")

# Sidebar for configuration
st.sidebar.header("API Configuration")
# Change local URL to live Render URL
api_url = st.sidebar.text_input("FastAPI URL", "https://intelligent-document-processing-e24n.onrender.com/api/v1/upload/")
# Main upload widget
uploaded_file = st.file_uploader("Upload an Internship Document (PDF, JPG, PNG)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info(f"File '{uploaded_file.name}' selected. Ready for AI processing.")
    
    if st.button("Analyze Document"):
        with st.spinner("🧠 AI is Extracting & Verifying... Please wait."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            try:
                # Call our FastAPI Backend
                response = requests.post(api_url, files=files)
                
                # --- NEW: Beautiful Duplicate Handling ---
                if response.status_code == 409:
                    st.warning(f"⚠️ **Duplicate Upload Detected!** The file '{uploaded_file.name}' has already been processed and verified in our database. AI processing skipped to save resources.")
                
                elif response.status_code != 200:
                    st.error(f"❌ Server Error: {response.json().get('detail', 'Unknown Error')}")
                
                else:
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
                        m2.metric("AI Confidence Score", f"{report.get('confidence_score', 0)}%")
                        
                        st.write(f"**Status:** {report.get('verification_status')}")
                        st.write(f"**Recommendation:** {report.get('recommended_action')}")
                        
                        if report.get("is_blurry"):
                            st.error("⚠️ Blurry Image Detected! Reduce camera shake.")
                        if report.get("expiry_alert"):
                            st.error("🚨 Document has Expired!")
                            
                        if report.get("missing_fields"):
                            st.warning(f"Missing Fields: {', '.join(report.get('missing_fields'))}")
                    
                    with col2:
                        document_type = data.get('document_type', 'Unknown')
                        st.subheader(f"Extracted Data ({document_type})")
                        
                        extracted = data.get("extracted_data", {})
                        
                        # Show main identity dynamically if it exists
                        if extracted.get("name"):
                            st.markdown(f"**👤 Name:** {extracted.get('name')}")
                        if extracted.get("father_name"):
                            st.markdown(f"**👨‍👦 Father's Name:** {extracted.get('father_name')}")
                        
                        # Display the rest of the JSON cleanly
                        st.json(extracted)
                    
                    st.subheader("Raw OCR Output")
                    with st.expander("Click to view raw OCR text before LLM cleanup"):
                        st.text(data.get("raw_text", ""))
                        
            except requests.exceptions.RequestException as e:
                st.error(f"API Connection Error: Make sure your FastAPI server is running (`uvicorn app.main:app --reload`).")