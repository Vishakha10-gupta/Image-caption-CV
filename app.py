import streamlit as st
from PIL import Image
from google import genai
from google.genai.errors import APIError

# --- Application Configuration ---
st.set_page_config(page_title="Computer Vision Image Parser", layout="centered")

# --- Initialize Client Securely from Streamlit Secrets ---
try:
    # Pulls directly from the Streamlit Cloud 3-dots Secrets panel
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Missing API Key. Please configure GOOGLE_API_KEY in your Streamlit Secrets panel via the 3-dots menu.")
    st.stop()

# --- Image Processing Components ---
def analyze_image_content(image_matrix):
    try:
        # Run content analysis pipeline using the secure client
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
    st.image(image, caption="Target Image", use_container_width=True)
    st.write("")

    if st.button("Run Image Analysis"):
        with st.spinner("Processing visual data matrix..."):
            parsed_text = analyze_image_content(image)

            if "Error" in parsed_text:
                st.error(parsed_text)
            else:
                st.success("Processing Complete!")
                st.info(f"**Generated Image Description:** {parsed_text}")
else:
    st.info("Please upload an image file to begin processing.")

st.markdown("---")
st.markdown("**Core Framework:** Digital Image Processing & Object Recognition System")
st.markdown("**Environment:** Managed Computer Vision Remote Pipeline Implementation")
