from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Union, List

# ---------- TipoUsuario ----------
class GenerosQuery(BaseModel):
    pk_id_genero: int
    genero: str
    icon: Optional[str] = None

# ESTADISTICAS PANEL PRINCIPAL

class MetricasValores(BaseModel):
    Total: int
    Delta: str
    Up: bool

class MetricasAdminPanel(BaseModel):
    Usuarios: Optional[MetricasValores] = None
    Libros: Optional[MetricasValores] = None
    PrestamosHoy: Optional[MetricasValores] = None

class TopLibrosAdminPanel(BaseModel):
    titulo: str
    prestamos: int

class EstadisticasAdminPanelA(BaseModel):
    Metricas: MetricasAdminPanel
    TopLibros: List[TopLibrosAdminPanel]
    SeriePrestamos: List[int]

