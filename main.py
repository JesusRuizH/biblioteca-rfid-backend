from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import prestamos, libros, copias_libros, usuarios, departamentos, tipo_usuario, generos

app = FastAPI(
    title="Biblio RFID API",
    description="API for managing library loans using RFID",
    version="1.0.0",
)

# Correct CORS middleware usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(prestamos.router)
app.include_router(libros.router)
app.include_router(copias_libros.router)
app.include_router(usuarios.router)
app.include_router(departamentos.router)
app.include_router(tipo_usuario.router)
app.include_router(generos.router)