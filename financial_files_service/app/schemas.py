from pydantic import BaseModel
from typing import List, Optional

class Transaccion(BaseModel):
    fecha: str
    descripcion: str
    monto: float
    tipo: str  # "ingreso" o "gasto"
    categoria: str # Ej: "Alimentación", "Salario", "Transporte"

class ReporteFinanciero(BaseModel):
    resumen: str
    transacciones: List[Transaccion]
    total_ingresos: float
    total_gastos: float