import sys
import subprocess

print("🔍 Image Caption CV - Dependency Check")
print("=" * 50)

dependencies = {
    "streamlit": "Streamlit Web Framework",
    "PIL": "Pillow - Image Processing",
    "torch": "PyTorch - Deep Learning",
    "transformers": "Hugging Face Transformers",
    "ultralytics": "YOLO - Object Detection",
    "cv2": "OpenCV - Computer Vision",
}

missing = []
installed = []

for module, description in dependencies.items():
    try:
        __import__(module)
        installed.append(f"✅ {module} - {description}")
    except ImportError:
        missing.append(f"❌ {module} - {description}")

print("\n".join(installed))

if missing:
    print("\n" + "=" * 50)
    print("Missing Dependencies:")
    print("=" * 50)
    print("\n".join(missing))
    print("\n" + "=" * 50)
    print("To install missing dependencies:")
    print("  Windows: setup.bat")
    print("  Linux/Mac: ./setup.sh")
    print("=" * 50)
    sys.exit(1)
else:
    print("\n" + "=" * 50)
    print("✅ All dependencies installed!")
    print("=" * 50)
    print("\nTo run the application:")
    print("  streamlit run app.py")
    sys.exit(0)
