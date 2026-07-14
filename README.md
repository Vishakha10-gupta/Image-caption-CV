
# Lightweight Image Captioning with Streamlit

Deployment Link:- 

https://image-caption-cv-af5kb4xml7dgfejpqhihm7.streamlit.app/

This project implements a lightweight image captioning solution using a pre-trained Vision-Encoder-Decoder model from Hugging Face Transformers, deployed as a web application using Streamlit.

## Project Overview

The goal of this project is to provide an easy-to-use tool for generating descriptive captions for images. It leverages the `nlpconnect/vit-gpt2-image-captioning` model, which combines a Vision Transformer (ViT) for image encoding and a GPT-2 model for text decoding. The application features a simple web interface built with Streamlit, allowing users to upload an image and instantly receive a generated caption.

## Features

- **Image Upload:** Easily upload images in JPG, JPEG, or PNG formats.
- **AI-Powered Captioning:** Utilizes a pre-trained state-of-the-art model for accurate and relevant caption generation.
- **Lightweight:** Designed to be efficient and suitable for deployment on platforms with limited resources.
- **Streamlit Web UI:** Intuitive and interactive user interface.

## Project Structure

```
my-image-captioning-project/
├── app.py                   # Main Streamlit application file
├── requirements.txt         # List of Python dependencies
├── README.md                # Project documentation
├── notebooks/               # (Optional) Jupyter/Colab notebooks for development and experimentation
│   └── image_captioning_development.ipynb
└── assets/                  # (Optional) Directory for example images or other static assets
    └── example_image.jpg
```

## Setup and Local Development

Follow these steps to set up and run the project locally:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/my-image-captioning-project.git
    cd my-image-captioning-project
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scriptsctivate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```

    The application will open in your web browser, typically at `http://localhost:8501`.

## Usage

1.  Open the Streamlit application in your web browser.
2.  Click the "Choose an image..." button to upload an image (JPG, JPEG, or PNG).
3.  Once the image is displayed, click the "Generate Caption" button.
4.  The generated caption will appear below the image.

## Model Details

This project uses the `nlpconnect/vit-gpt2-image-captioning` model. This model consists of:

- **Encoder:** A Vision Transformer (ViT) that processes the input image.
- **Decoder:** A GPT-2 language model that generates a textual caption based on the visual features provided by the encoder.

For more details on the model, refer to its [Hugging Face Model Card](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning).

## Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) for providing state-of-the-art NLP and vision models.
- [Streamlit](https://streamlit.io/) for making web application development in Python incredibly easy.
- This project was developed as part of a Google Colab initiative.

## License

[Optional: e.g., MIT License or Apache 2.0 License]
