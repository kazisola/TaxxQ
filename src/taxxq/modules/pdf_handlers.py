from fastapi import UploadFile
import os
import shutil

UPLOAD_DIR = "./upload_docs"

def save_uploaded_files(files: list[UploadFile]) -> list[str]:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = []

    for file in files:
        if not file.filename:
            raise ValueError("uploaded file must have a filename")
        temp_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_path.append(temp_path)

    return file_path