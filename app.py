import streamlit as st
from PIL import Image
import io
from ultralytics import YOLO
from model import generate_caption_with_detection

st.set_page_config(
    page_title="AI Image Captioning",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        text-align: center;
        color: #00ff88;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🖼️ AI Image Captioning")
st.markdown("### Upload an image to generate intelligent captions powered by AI")

# Create two columns for better layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        label_visibility="collapsed"
    )

with col2:
    st.subheader("Preview")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="Uploaded Image")

# Process and generate caption
if uploaded_file is not None:
    with st.spinner("🔄 Analyzing image and generating caption..."):
        try:
            # Convert uploaded file to PIL Image
            image = Image.open(uploaded_file)
            
            # Generate caption with object detection
            caption, detections = generate_caption_with_detection(image)
            
            # Display results
            st.success("✅ Caption generated successfully!")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📝 Generated Caption")
                st.markdown(f"### {caption}")
            
            with col2:
                st.subheader("🎯 Detected Objects")
                if detections:
                    for obj in detections:
                        st.markdown(f"- **{obj['name']}** (confidence: {obj['confidence']:.2%})")
                else:
                    st.info("No objects detected in the image.")
            
            # Additional info
            st.divider()
            with st.expander("📊 Model Information"):
                st.markdown("""
                - **Vision Model**: YOLOv8 Nano (Transfer Learning)
                - **Captioning Model**: BLIP (Salesforce)
                - **Framework**: Streamlit
                """)
        
        except Exception as e:
            st.error(f"❌ Error generating caption: {str(e)}")
            st.info("Please ensure the image format is supported and try again.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True,use_reloader=False)
