#!/bin/bash

# Linux/Mac Setup Script for Image Caption CV

echo ""
echo "===================================="
echo "Image Caption CV - Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

echo "Installing PyTorch CPU version..."
pip install torch torchvision torchaudio

echo ""
echo "Installing other dependencies..."
pip install -r requirements.txt

echo ""
echo "===================================="
echo "Setup Complete!"
echo "===================================="
echo ""
echo "To run the application:"
echo "  streamlit run app.py"
echo ""
