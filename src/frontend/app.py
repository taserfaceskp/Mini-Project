import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(
    page_title="Threat Detectives - Phishing Detection Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Threat Detectives Phishing Detection Dashboard")
st.write("Real-time Multimodal AI Phishing Detection and Local SLM Triage")

st.sidebar.header("Pipeline Configurations")
api_host = st.sidebar.text_input("API Endpoint", "http://127.0.0.1:8000/api/v1")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Payload Details")
    email_text = st.text_area("Suspicious Email Text", "", height=150, placeholder="Paste the email body here...")
    uploaded_file = st.file_uploader("Upload Webpage Screenshot", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Webpage Screenshot", use_column_width=True)

with col2:
    st.subheader("Multimodal Threat Assessment")
    
    if st.button("Analyze Payload", type="primary"):
        if not email_text or not uploaded_file:
            st.warning("Please provide both email text and a screenshot to perform dual-modal analysis.")
        else:
            with st.spinner("Running AI Pipeline..."):
                try:
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format=uploaded_file.type.split("/")[-1].upper())
                    img_bytes = img_byte_arr.getvalue()
                    
                    files = {"screenshot": (uploaded_file.name, img_bytes, uploaded_file.type)}
                    data = {"email_text": email_text}
                    
                    response = requests.post(f"{api_host}/analyze", data=data, files=files, timeout=15)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Analysis Complete!")
                        
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Threat Score", f"{result.get('threat_score', 0.0)}/10.0")
                        m2.metric("Detected Brand", result.get('brand_detected', "None"))
                        m3.metric("Domain Matches Brand?", "Yes" if result.get('domain_match', True) else "No")
                        
                        st.subheader("Local SLM Threat Explanation (Ollama)")
                        st.info(result.get("explanation", "No summary generated."))
                    else:
                        st.error(f"API Server returned status code {response.status_code}")
                except Exception as e:
                    st.error(f"Failed to connect to FastAPI backend: {str(e)}")
