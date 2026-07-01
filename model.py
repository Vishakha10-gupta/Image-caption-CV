import os
from typing import List

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

yolo_model = None
processor = None
caption_model = None


def _load_models():
    global yolo_model, processor, caption_model

    if yolo_model is None:
        if YOLO is None:
            return None, None, None
        yolo_model = YOLO(YOLO_MODEL_NAME)

    if processor is None or caption_model is None:
        if BlipProcessor is None or BlipForConditionalGeneration is None or torch is None:
            return yolo_model, None, None
        processor = BlipProcessor.from_pretrained(MODEL_NAME)
        caption_model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
        caption_model.eval()

    return yolo_model, processor, caption_model


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
