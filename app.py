from flask import Flask, render_template, request, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename

from model import image_caption_pipeline

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return render_template("index.html", error="No image uploaded."), 400

    file = request.files["image"]
    if file.filename == "":
        return render_template("index.html", error="No file selected."), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        caption = image_caption_pipeline(filepath)
    except Exception as exc:
        return render_template(
            "index.html",
            error=f"Caption generation failed: {exc}",
            image=url_for("uploaded_file", filename=filename),
        ), 500

    image_url = url_for("uploaded_file", filename=filename)
    return render_template("index.html", image=image_url, caption=caption)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True,use_reloader=False)
