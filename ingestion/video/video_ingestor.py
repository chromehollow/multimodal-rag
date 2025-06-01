from moviepy.editor import VideoFileClip
from ingestion.audio.audio_ingestor import transcribe_audio

def extract_text_from_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)
    return transcribe_audio(audio_path)
