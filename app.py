import streamlit as st
from PIL import Image
from transformers import VisionEncoderDecoderModel, AutoTokenizer, AutoImageProcessor
import torch
import os

# --- System Configuration --- #
SYSTEM_CHECKPOINT = "nlpconnect/vit-gpt2-image-captioning"

# --- Image Processing Components ---
@st.cache_resource
def load_processing_components():
    model = VisionEncoderDecoderModel.from_pretrained(SYSTEM_CHECKPOINT)
    image_processor = AutoImageProcessor.from_pretrained(SYSTEM_CHECKPOINT)
    model_tokenizer = AutoTokenizer.from_pretrained(SYSTEM_CHECKPOINT)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    model.config.decoder_start_token_id = model_tokenizer.bos_token_id
    model.config.pad_token_id = model_tokenizer.pad_token_id
    model.config.vocab_size = model_tokenizer.vocab_size
    model.config.max_length = 32
    model.config.num_beams = 4
    model.config.early_stopping = True
    model.config.no_repeat_ngram_size = 3
    model.config.length_penalty = 2.0
    
    return model, image_processor, model_tokenizer, device

model, image_processor, model_tokenizer, device = load_processing_components()

# --- Image Analysis Function ---
def analyze_image_content(image):
    pixel_values = image_processor(images=image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)
    
    output_ids = model.generate(
        pixel_values, 
        num_beams=model.config.num_beams, 
        max_length=model.config.max_length
    )
    analysis_result = model_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return analysis_result

# --- Streamlit UI ---
st.set_page_config(page_title="Computer Vision Image Parser", layout="centered")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("🔑 Authentication")
    system_key = st.text_input("Enter System Access Key", type="password", help="Provide your developer access token to run the parser.")
    
    if system_key:
        os.environ["SYSTEM_ACCESS_KEY"] = system_key
        st.success("Access key authorized.")
    else:
        st.warning("Please enter your system access key.")

st.title("🖼️ Automated Image Content Parser")
st.write("Upload a digital image file to execute structural content parsing and generate a description.")

# Image Upload
uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Target Image", use_container_width=True)
    st.write("")
    
    if st.button("Run Image Analysis"):
        if not system_key:
            st.error("Access key required. Please complete authentication in the sidebar panel.")
        else:
            with st.spinner("Processing visual data matrix..."):
                parsed_text = analyze_image_content(image)
                st.success("Processing Complete!")
                st.info(f"**Generated Image Description:** {parsed_text}")
else:
    st.info("Please upload an image file to begin processing.")

st.markdown("---")
st.markdown("**Core Framework:** Digital Image Processing & Object Recognition System")
st.markdown("**Environment:** Google Colab Computer Vision Pipeline Implementation")
