import streamlit as st
from PIL import Image
from google import genai
from google.genai.errors import APIError

# --- Image Processing Components ---
def analyze_image_content(image, access_token):
    try:
        # Initialize the processing client using the system key
        client = genai.Client(api_key=access_token)
        
        # Run content analysis pipeline 
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                image, 
                "Provide a highly accurate, brief description of the structural content and layout of this image."
            ]
        )
        return response.text
    except APIError as e:
        return f"Authentication Error: Verification failed. ({e.message})"
    except Exception as e:
        return f"System Error: Failed to execute content analysis path. ({str(e)})"

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="Computer Vision Image Parser", layout="centered")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("🔑 Authentication")
    system_key = st.text_input(
        "Enter System Access Key", 
        type="password", 
        help="Provide your developer access token from the systems portal to run the parser."
    )
    
    if system_key:
        st.success("Access key structured.")
    else:
        st.warning("Please enter your system access key to initialize.")

st.title("🖼️ Automated Image Content Parser")
st.write("Upload a digital image file to execute structural content parsing and generate a description.")

# Image Upload Block
uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert uploaded data stream to image structure
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Target Image", use_container_width=True)
    st.write("")
    
    if st.button("Run Image Analysis"):
        if not system_key:
            st.error("Access key required. Please complete authentication in the sidebar panel.")
        else:
            with st.spinner("Processing visual data matrix..."):
                parsed_text = analyze_image_content(image, system_key)
                
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
