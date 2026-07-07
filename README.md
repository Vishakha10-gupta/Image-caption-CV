# 🖼️ AI Image Captioning with YOLO Transfer Learning

A Streamlit web application that uses **YOLO nano (transfer learning)** for object detection and **BLIP** for intelligent image captioning.

## Features

✨ **Key Capabilities:**
- Upload images in multiple formats (JPG, PNG, BMP, WebP)
- Automatic object detection using YOLOv8 Nano
- AI-powered caption generation using BLIP
- Context-aware captions based on detected objects
- Beautiful, responsive Streamlit UI
- Production-ready deployment

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup - Windows (Recommended)

Simply run the setup script:
```bash
setup.bat
```

This will automatically:
1. Install PyTorch CPU version (optimized for Windows)
2. Install all other dependencies
3. Prepare the environment

### Setup - Linux/Mac

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup (All Platforms)

1. **Clone/Navigate to the project:**
   ```bash
   cd Image-caption-CV
   ```

2. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install PyTorch:**
   ```bash
   # CPU version (recommended for most users):
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   
   # GPU version (CUDA 12.1):
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

4. **Install other dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application locally:**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`

## Usage

1. **Upload an Image**: Click the upload button and select an image (JPG, PNG, BMP, or WebP)
2. **View Preview**: The image will be displayed in the preview panel
3. **Get Caption**: The app automatically detects objects and generates a caption
4. **View Results**: See the generated caption and list of detected objects

## Models Used

| Model | Purpose | Source |
|-------|---------|--------|
| **YOLOv8 Nano** | Object Detection (Transfer Learning) | Ultralytics |
| **BLIP** | Image Captioning | Salesforce |

## Deployment

### Option 1: Streamlit Community Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create a new app and select your repository
4. Streamlit will automatically detect `app.py` and deploy

### Option 2: Heroku

1. Create `Procfile`:
   ```
   web: streamlit run --server.port $PORT --server.address 0.0.0.0 app.py
   ```

2. Deploy:
   ```bash
   git push heroku main
   ```

### Option 3: Docker

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD streamlit run --server.port 8501 --server.address 0.0.0.0 app.py
   ```

2. Build and run:
   ```bash
   docker build -t caption-cv .
   docker run -p 8501:8501 caption-cv
   ```

## Performance Tips

- **First Run**: Models are downloaded and cached (~2-3 GB of storage)
- **Caching**: Streamlit caches loaded models for faster subsequent runs
- **GPU**: Install CUDA version of PyTorch for faster inference:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

## File Structure

```
Image-caption-CV/
├── app.py                 # Streamlit main application
├── model.py               # Model loading and inference logic
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── templates/             # (Optional for Flask) Can be removed
└── README.md              # This file
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Models take long to download | This is normal on first run (~2-3 GB). They're cached for future runs. |
| Out of memory | Use GPU or reduce batch size in inference |
| CUDA not found | Install CPU version of PyTorch or CPU version works too |

## API Reference

### Main Functions

```python
generate_caption_with_detection(image: Image.Image) -> Tuple[str, List[Dict]]
```
- **Input**: PIL Image object
- **Output**: Tuple of (caption_string, detections_list)

```python
image_caption_pipeline(filepath: str) -> str
```
- **Input**: File path to image
- **Output**: Caption string

## Environment Variables (Optional)

```bash
export LOG_LEVEL=info
```

## Future Enhancements

- [ ] Fine-tune YOLO on custom dataset
- [ ] Add batch processing for multiple images
- [ ] Export captions as JSON/CSV
- [ ] Support for video captioning
- [ ] Multi-language caption support
- [ ] Confidence filtering UI controls

## License

MIT

## Support

For issues or questions, please check the [Streamlit documentation](https://docs.streamlit.io)

---

Built with ❤️ using Streamlit, YOLO, and BLIP
