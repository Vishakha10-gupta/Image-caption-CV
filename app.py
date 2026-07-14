import streamlit as st
from PIL import Image
from google import genai
from google.genai.errors import APIError

# --- Application Configuration ---
st.set_page_config(page_title="Computer Vision Image Parser", layout="wide")

# --- Initialize Client Securely from Streamlit Secrets ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Missing API Key. Please configure GOOGLE_API_KEY in your Streamlit Secrets panel via the 3-dots menu.")
    st.stop()

# --- Image Processing Components ---
def analyze_image_content(image_matrix):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                image_matrix, 
                "Provide a highly accurate, brief description of the structural content and layout of this image."
            ]
        )
        return response.text
    except APIError as e:
        return f"Authentication Error: Verification failed. ({e.message})"
    except Exception as e:
        return f"System Error: Failed to execute content analysis path. ({str(e)})"

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Authentication")
    st.success("System connection secure. Ready to parse.")

st.title("Automated Image Content Parser")
st.write("Upload a digital image file to execute structural content parsing and generate a description.")

# Image Upload Block
uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert uploaded data stream to image structure
    image = Image.open(uploaded_file).convert("RGB")
    st.write("")
    
    # Create two equal-width columns for side-by-side view
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Target Image")
        st.image(image, use_container_width=True)
        analyze_button = st.button("Run Image Analysis", use_container_width=True)
        
    with col2:
        st.subheader("Analysis Output")
        if analyze_button:
            with st.spinner("Processing visual data matrix..."):
                parsed_text = analyze_image_content(image)
                
                if "Error" in parsed_text:
                    st.error(parsed_text)
                else:
                    st.success("Processing Complete!")
                    st.info(f"**Generated Image Description:** {parsed_text}")
        else:
            st.info("Click the Run Image Analysis button to view results here.")
else:
    st.info("Please upload an image file to begin processing.")

st.markdown("---")
st.markdown("**Core Framework:** Digital Image Processing & Object Recognition System")
st.markdown("**Environment:** Managed Computer Vision Remote Pipeline Implementation")
