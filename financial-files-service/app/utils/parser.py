import pypdf
from fastapi import UploadFile


def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Lee un archivo PDF en memoria y extrae su texto.
    """
    reader = pypdf.PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text