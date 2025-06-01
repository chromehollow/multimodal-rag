import os
from ingestion.text_ingestor import extract_text
from ingestion.audio.audio_ingestor import transcribe_audio
from ingestion.images.image_ingestor import extract_text_from_image

from ingestion.video.video_ingestor import extract_text_from_video

def auto_ingest(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in [".txt"]:
        return extract_text(file_path)
    elif ext in [".mp3", ".wav"]:
        return transcribe_audio(file_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)
    elif ext in [".mp4"]:
        return extract_text_from_video(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
