# Deployment Guides

## 🚀 Streamlit Community Cloud (Recommended & Free)

### Steps:
1. Push your code to GitHub (public repo)
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Connect GitHub repo
5. Select repository, branch, and main file (`app.py`)
6. Deploy!

### Benefits:
- ✅ Free hosting
- ✅ Automatic redeploys on Git push
- ✅ Custom domain support (paid)
- ✅ SSL included
- ✅ No server management

**Estimated time to deploy:** 2-5 minutes

---

## 🐳 Docker Deployment

### Local Docker Testing:

1. Create `Dockerfile` in project root (already provided below)
2. Build image:
   ```bash
   docker build -t caption-cv:latest .
   ```
3. Run locally:
   ```bash
   docker run -p 8501:8501 caption-cv:latest
   ```
4. Visit `http://localhost:8501`

### Production Docker Deployment:

Push to Docker Hub or any registry:
```bash
docker tag caption-cv:latest username/caption-cv:latest
docker push username/caption-cv:latest
```

Then deploy using:
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- Kubernetes
- DigitalOcean App Platform

### Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install PyTorch CPU
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app.py .
COPY model.py .
COPY .streamlit/ .streamlit/

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## ☁️ Hugging Face Spaces

### Steps:
1. Create account at [huggingface.co](https://huggingface.co)
2. Create new Space
3. Choose "Streamlit" as SDK
4. Connect GitHub repo or upload files
5. Add `README.md` with app description
6. Deploy!

### Benefits:
- ✅ Free tier available
- ✅ Easy integration
- ✅ GPU support available
- ✅ No credit card for free tier

---

## 🔵 AWS Deployment

### Option 1: Elastic Beanstalk

1. Install EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Initialize:
   ```bash
   eb init -p python-3.11 caption-cv
   ```

3. Create environment:
   ```bash
   eb create caption-cv-env
   ```

4. Deploy:
   ```bash
   eb deploy
   ```

### Option 2: AWS App Runner

1. Push to ECR (Elastic Container Registry)
2. Go to App Runner console
3. Create new service
4. Select ECR image
5. Deploy!

---

## 🟠 Heroku Deployment (Legacy - Paid Now)

### Note: Heroku free tier is discontinued

Still works if you have credits:

1. Create `Procfile`:
   ```
   web: streamlit run --server.port=$PORT --server.address=0.0.0.0 app.py
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.0
   ```

3. Deploy:
   ```bash
   heroku login
   heroku create caption-cv
   git push heroku main
   ```

---

## 🟢 Google Cloud Run

### Using Docker:

1. Build and push image:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/caption-cv
   ```

2. Deploy:
   ```bash
   gcloud run deploy caption-cv \
     --image gcr.io/PROJECT-ID/caption-cv \
     --platform managed \
     --region us-central1 \
     --memory 2Gi
   ```

3. Access at provided URL

### Benefits:
- ✅ Serverless (pay per request)
- ✅ Auto-scaling
- ✅ No infrastructure management

---

## 🟣 DigitalOcean App Platform

1. Push code to GitHub
2. Sign up/Login to DigitalOcean
3. Create new App
4. Connect GitHub
5. Select repository
6. Choose "Python" > "Streamlit"
7. Deploy!

**Pricing:** $12/month (starter plan)

---

## 📊 Deployment Comparison

| Platform | Cost | Setup Time | Scaling | GPU Support |
|----------|------|-----------|---------|------------|
| Streamlit Cloud | Free/Paid | 2 min | Auto | No* |
| HF Spaces | Free/Paid | 3 min | Auto | Yes* |
| Docker + Registry | Varies | 10 min | Manual | Yes |
| AWS App Runner | Paid | 15 min | Auto | Yes |
| Google Cloud Run | Paid | 10 min | Auto | Yes |
| DigitalOcean | $12/mo | 5 min | Manual | No |
| Heroku | Paid | 5 min | Auto | No |

\* Available on paid tiers

---

## 🔧 Environment Variables

For any deployment, set these environment variables:

```bash
STREAMLIT_SERVER_MAXUPLOADSIZE=200
STREAMLIT_SERVER_ENABLEXSRFPROTECTION=true
STREAMLIT_LOGGER_LEVEL=info
```

---

## 📈 Performance Optimization for Deployment

1. **Cache Models**: Models are cached with `@st.cache_resource`
2. **CPU Only**: Default to CPU inference (cheaper on cloud)
3. **Image Compression**: Input images are optimized automatically
4. **Memory**: Allocate at least 2GB RAM
5. **Storage**: Reserve 3GB for model downloads

---

## 🆘 Troubleshooting Deployments

### Issue: Models not downloading
**Solution**: Increase deployment timeout or pre-cache models

### Issue: Out of memory
**Solution**: Increase instance size or use CPU-optimized deployment

### Issue: Slow response time
**Solution**: Enable GPU, reduce image size, or use model quantization

---

## 🎯 Recommended for Beginners

**Streamlit Community Cloud** - It's the easiest!
```bash
git push  # Deploy!
```

---

For more info, visit: [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud)
