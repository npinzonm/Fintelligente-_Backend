# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 1. Importación clave

from dotenv import load_dotenv
from typing import List

from financial_files_service.app.routers import files

# Cargar variables de entorno al iniciar
load_dotenv()

app = FastAPI(title="Financial Files Service")

# --- CONFIGURACIÓN DE CORS ---

# Lista de orígenes permitidos (Tu frontend local y futuro despliegue)
origins: List[str] = [
    "http://localhost:5173",  # Frontend local de React/Vite
    "http://127.0.0.1:5173",
    "https://fintelligente-nxwwpyk70-npinzonms-projects.vercel.app",
    "https://fintelligente-faowu83or-npinzonms-projects.vercel.app",
    "https://fintelligente-nv.vercel.app/",
    # 🚨 IMPORTANTE: Añade tu URL de Vercel aquí después del despliegue en Render
    # Por ejemplo: "https://mi-app-financiera.vercel.app"
]

# 2. Agregar el Middleware de CORS a la aplicación principal
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUSIÓN DEL ROUTER ---

# Incluir el router que creamos (donde está /upload-financial-pdf)
app.include_router(files.router)

@app.get("/")
def read_root():
    return {"message": "API de Finanzas con IA activa"}