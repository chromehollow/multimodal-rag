from pathlib import Path
import fitz  # PyMuPDF

def extract_text(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    else:
        raise ValueError("Unsupported file type: " + ext)
