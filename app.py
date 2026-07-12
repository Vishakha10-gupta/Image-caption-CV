
import streamlit as st
from PIL import Image
from transformers import VisionEncoderDecoderModel, AutoTokenizer, AutoImageProcessor
import torch
import os

# --- Configuration --- #
MODEL_CHECKPOINT = "nlpconnect/vit-gpt2-image-captioning"

# --- Load Model and Components (Cached) ---
@st.cache_resource
def load_model_components():
    model = VisionEncoderDecoderModel.from_pretrained(MODEL_CHECKPOINT)
    image_processor = AutoImageProcessor.from_pretrained(MODEL_CHECKPOINT)
    model_tokenizer = AutoTokenizer.from_pretrained(MODEL_CHECKPOINT)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # Set generation parameters
    model.config.decoder_start_token_id = model_tokenizer.bos_token_id
    model.config.pad_token_id = model_tokenizer.pad_token_id
    model.config.vocab_size = model_tokenizer.vocab_size
    model.config.max_length = 32 # A reasonable max length for captions
    model.config.num_beams = 4
    model.config.early_stopping = True
    model.config.no_repeat_ngram_size = 3
    model.config.length_penalty = 2.0
    
    return model, image_processor, model_tokenizer, device

model, image_processor, model_tokenizer, device = load_model_components()

# --- Caption Generation Function ---
def generate_caption(image):
    pixel_values = image_processor(images=image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)
    
    output_ids = model.generate(pixel_values, 
                                num_beams=model.config.num_beams, 
                                max_length=model.config.max_length)
    
    caption = model_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return caption

# --- Streamlit UI ---
st.set_page_config(page_title="Image Captioning App", layout="centered")
st.title("🖼️ Lightweight Image Captioning")
st.write("Upload an image and let the AI generate a descriptive caption!")

# Image Upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("")
    
    if st.button("Generate Caption"):
        with st.spinner("Generating caption..."):
            caption = generate_caption(image)
            st.success("Caption Generated!")
            st.info(f"**Caption:** {caption}")
else:
    st.info("Please upload an image to get started.")

st.markdown("---")
st.markdown("**Model:** `nlpconnect/vit-gpt2-image-captioning` from Hugging Face Transformers")
st.markdown("**Developed for a Google Colab Image Captioning project.**")
