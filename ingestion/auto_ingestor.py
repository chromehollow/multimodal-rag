import os
import fitz  # PyMuPDF

from ingestion.text_ingestor import extract_text
from ingestion.audio.audio_ingestor import transcribe_audio
from ingestion.images.image_ingestor import extract_text_from_image
from ingestion.video.video_ingestor import extract_text_from_video

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def auto_ingest(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext in [".txt", ".md", ".json"]:
        return extract_text(file_path)

    elif ext in [".mp3", ".wav", ".m4a"]:
        return transcribe_audio(file_path)

    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        return extract_text_from_image(file_path)

    elif ext in [".mp4", ".mov", ".avi"]:
        return extract_text_from_video(file_path)

    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
