# ⚡ Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Prepare
```bash
cd Image-caption-CV
```

### Step 2: Install (Choose your OS)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Run
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📸 Using the App

1. **Upload** an image (JPG, PNG, BMP, WebP)
2. **Wait** for processing (usually 5-10 seconds)
3. **View** the caption and detected objects

---

## 🐳 Quick Docker Setup

```bash
# Build
docker build -t caption-cv .

# Run
docker run -p 8501:8501 caption-cv

# Or with Docker Compose
docker-compose up
```

Then visit: `http://localhost:8501`

---

## ☁️ Quick Cloud Deployment

### Streamlit Community Cloud (Easiest)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select your repo
4. Done! 🎉

### Hugging Face Spaces
1. Create Space
2. Upload files
3. Done! 🎉

See `DEPLOYMENT.md` for more options.

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Models downloading too slow** | First run takes 5-10 min, but cached after |
| **Out of memory errors** | Close other apps or allocate more RAM |
| **Import errors** | Run `python check_dependencies.py` |
| **Port 8501 in use** | `streamlit run app.py --server.port 8502` |

---

## 📚 Full Documentation

- Setup: [README.md](README.md)
- Deployment: [DEPLOYMENT.md](DEPLOYMENT.md)
- Dependencies: Run `python check_dependencies.py`

---

## 🎯 What This App Does

✅ **Detects objects** in images using YOLOv8 Nano  
✅ **Generates captions** using BLIP model  
✅ **Context-aware** - captions reference detected objects  
✅ **Fast** - runs on CPU  
✅ **Production ready** - Streamlit deployment optimized  

---

Enjoy! 🚀
