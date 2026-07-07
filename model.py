import os
from typing import List, Tuple, Dict
import streamlit as st

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

try:
    import torch
except ImportError:  # pragma: no cover
    torch = None

try:
    from ultralytics import YOLO
except ImportError:  # pragma: no cover
    YOLO = None

try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
except ImportError:  # pragma: no cover
    BlipProcessor = None
    BlipForConditionalGeneration = None


MODEL_NAME = "Salesforce/blip-image-captioning-base"
YOLO_MODEL_NAME = "yolov8n.pt"


@st.cache_resource
def _load_yolo_model():
    """Load YOLO nano model with caching for Streamlit."""
    if YOLO is None:
        raise ImportError("ultralytics not installed. Install with: pip install ultralytics")
    return YOLO(YOLO_MODEL_NAME)


@st.cache_resource
def _load_caption_model():
    """Load BLIP caption model with caching for Streamlit."""
    if BlipProcessor is None or BlipForConditionalGeneration is None:
        raise ImportError("transformers not installed. Install with: pip install transformers")
    if torch is None:
        raise ImportError("torch not installed. Install with: pip install torch")
    
    processor = BlipProcessor.from_pretrained(MODEL_NAME)
    caption_model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
    caption_model.eval()
    
    return processor, caption_model


def _detect_objects(yolo_model, image: Image.Image, conf_threshold: float = 0.45) -> List[Dict]:
    """
    Detect objects in image using YOLO nano model.
    
    Args:
        yolo_model: Loaded YOLO model
        image: PIL Image object
        conf_threshold: Confidence threshold for detection
    
    Returns:
        List of detected objects with names and confidence scores
    """
    try:
        results = yolo_model(image, conf=conf_threshold, verbose=False)
        detections = []
        
        if results and len(results) > 0:
            result = results[0]
            if hasattr(result, 'boxes') and result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    class_name = result.names[class_id]
                    
                    detections.append({
                        "name": class_name,
                        "confidence": confidence,
                        "class_id": class_id
                    })
        
        return detections
    except Exception as e:
        print(f"Error in object detection: {str(e)}")
        return []


def _generate_caption(processor, caption_model, image: Image.Image, context: str = None) -> str:
    """
    Generate caption for image using BLIP model.
    
    Args:
        processor: BLIP processor
        caption_model: BLIP caption model
        image: PIL Image object
        context: Optional context text to guide caption generation
    
    Returns:
        Generated caption string
    """
    try:
        # Convert image to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Prepare inputs
        if context:
            inputs = processor(image, text=context, return_tensors="pt")
        else:
            inputs = processor(image, return_tensors="pt")
        
        # Generate caption
        with torch.no_grad():
            out = caption_model.generate(**inputs, max_length=100, num_beams=5)
        
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        print(f"Error in caption generation: {str(e)}")
        return "Unable to generate caption"


def generate_caption_with_detection(image: Image.Image) -> Tuple[str, List[Dict]]:
    """
    Main function: Detect objects and generate image caption.
    
    Args:
        image: PIL Image object
    
    Returns:
        Tuple of (caption, detected_objects)
    """
    # Load models
    yolo_model = _load_yolo_model()
    processor, caption_model = _load_caption_model()
    
    # Detect objects
    detections = _detect_objects(yolo_model, image)
    
    # Generate context from detections for better captioning
    context = None
    if detections:
        detected_names = ", ".join([d["name"] for d in detections[:5]])  # Top 5 detections
        context = f"a photo with {detected_names}"
    
    # Generate caption
    caption = _generate_caption(processor, caption_model, image, context)
    
    return caption, detections


def image_caption_pipeline(filepath: str) -> str:
    """
    Legacy function for backward compatibility.
    Load image from file path and generate caption.
    """
    if Image is None:
        raise ImportError("Pillow not installed")
    
    image = Image.open(filepath)
    caption, _ = generate_caption_with_detection(image)
    return caption


def preprocess_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise ValueError(f"Image file not found: {image_path}")
    return image_path


def extract_features(image_path: str) -> List[str]:
    model = _load_models()[0]
    if model is None:
        return []

    results = model(image_path)

    objects = []
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            objects.append(label)

    return sorted(set(objects))


def _fallback_caption(image_path: str, objects: List[str]) -> str:
    try:
        if Image is not None:
            with Image.open(image_path) as raw_image:
                raw_image = raw_image.convert("RGB")
                width, height = raw_image.size
                return f"A colorful image with a {width}x{height} composition and a clear subject."
    except Exception:
        pass

    if objects:
        object_text = ", ".join(objects[:4])
        return f"A scene featuring {object_text}."

    return "A detailed image captured for captioning."


def generate_caption(image_path: str, objects: List[str]) -> str:
    _, processor_instance, model_instance = _load_models()

    if processor_instance is not None and model_instance is not None and torch is not None:
        raw_image = Image.open(image_path).convert("RGB")
        text_prompt = "Objects detected: " + ", ".join(objects) if objects else "Describe this image."

        inputs = processor_instance(
            raw_image,
            text=text_prompt,
            return_tensors="pt",
        )

        with torch.no_grad():
            out = model_instance.generate(**inputs)

        return processor_instance.decode(out[0], skip_special_tokens=True)

    return _fallback_caption(image_path, objects)


def post_process(caption: str) -> str:
    caption = caption.strip().capitalize()
    if not caption.endswith("."):
        caption += "."
    return caption


def image_caption_pipeline(image_path: str) -> str:
    image_path = preprocess_image(image_path)
    objects = extract_features(image_path)
    caption = generate_caption(image_path, objects)
    return post_process(caption)
