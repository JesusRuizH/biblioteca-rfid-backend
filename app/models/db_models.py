from io import BufferedReader

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Union, List
from pocketbase.models import FileUpload

# ---------- TipoUsuario ----------
class TipoUsuario(BaseModel):
    id: Optional[str]
    pk_id_tipo_usuario: int
    rol: str
    created_at: Union[Optional[datetime], str] = None
    updated_at: Union[Optional[datetime], str] = None


# ---------- Usuarios ----------
class Usuario(BaseModel):
    id: Optional[str]
    pk_id_usuario: int
    nombre_usuario: str
    password: Optional[str] = None
    passwordConfirm: Optional[str] = None
    verified: bool
    email: str
    fk_id_tipo_usuario: str
    fecha_nacimiento: Union[Optional[datetime], str] = None
    created_at: Union[Optional[datetime], str] = None
    updated_at: Union[Optional[datetime], str] = None


# ---------- Departamento ----------
class Departamento(BaseModel):
    id: Optional[str]
    pk_id_departamento: int
    numero: int
    nombre: str
    created_at: Union[Optional[datetime], str] = None
    updated_at: Union[Optional[datetime], str] = None


# ---------- Libros ----------
class Libro(BaseModel):
    id: Optional[str]
    pk_id_libro: int
    titulo: str
    autor: str
    fecha_publicacion: Union[Optional[datetime], str] = None
    ruta_img: Optional[str] = None
    copias: Optional[int] = 0
    fk_id_departamento: Optional[str] = None
    fk_id_genero: Optional[Union[str, List[str]]] = None
    created_at: Union[Optional[datetime], str] = None
    updated_at: Union[Optional[datetime], str] = None

# ---------- Generos ----------

class Generos(BaseModel):
    id: Optional[str]
    pk_id_genero: int
    genero: str
    icon: Optional[str]
    created_at: Union[Optional[datetime], str] = None
    updated_at: Union[Optional[datetime], str] = None


# ---------- CopiasLibro ----------
class CopiaLibro(BaseModel):
    id: Optional[str]
    pk_id_copia: int
    fk_id_libro: str
    isbn: str
    rfid_tag: str
    disponibilidad: bool
    created_at: Union[Optional[datetime], str] = None
    updated_at: Union[Optional[datetime], str] = None


# ---------- Prestamos ----------
class Prestamo(BaseModel):
    id: Optional[str]
    pk_id_prestamo: int
    fk_id_copia: str
    fk_id_usuario: str
    fecha_prestamo: Union[Optional[datetime], str] = None
    fecha_entrega: Union[Optional[datetime], str] = None
    dias_restantes: Optional[int]
    estatus_entrega: Optional[bool]
    created_at: Union[Optional[datetime], str] = None
    updated_at: Union[Optional[datetime], str] = None
