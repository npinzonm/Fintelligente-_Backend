from fastapi import APIRouter, UploadFile, File, HTTPException
from ..utils.parser import extract_text_from_pdf
from ..ai_reader import analyze_financial_text
from ..schemas import ReporteFinanciero

router = APIRouter()


@router.post("/upload-financial-pdf", response_model=ReporteFinanciero)
async def upload_file(file: UploadFile = File(...)):
    """
    Recibe un PDF, extrae texto, lo analiza con Gemini y devuelve JSON clasificado.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

    try:
        # 1. Extraer texto
        text_content = extract_text_from_pdf(file)

        # 2. Procesar con IA
        result = analyze_financial_text(text_content)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))