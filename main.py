from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import prestamos, libros, copias_libros, usuarios, departamentos, tipo_usuario, generos, recomendador, estadisticas, recomendaciones_usuario
from contextlib import asynccontextmanager
from app.schedulers.scheduler import start_scheduler, scheduler, get_admin_token, check_expiring_loans
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.SCHEDULER_ENABLED:
        await get_admin_token()
        start_scheduler()
    yield
    if settings.SCHEDULER_ENABLED:
        scheduler.shutdown()

app = FastAPI(
    title="Biblio RFID API",
    description="API for managing library loans using RFID",
    version="1.0.0",
    lifespan= lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(prestamos.router)
app.include_router(libros.router)
app.include_router(copias_libros.router)
app.include_router(usuarios.router)
app.include_router(departamentos.router)
app.include_router(tipo_usuario.router)
app.include_router(generos.router)
app.include_router(recomendador.router)
app.include_router(estadisticas.router)
app.include_router(recomendaciones_usuario.router)