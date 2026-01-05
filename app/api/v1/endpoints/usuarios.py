from typing import List

from pocketbase.utils import ClientResponseError

from fastapi import APIRouter, HTTPException, status
from app.pb_clients.usuarios import (
    db_get_usuario,
    db_create_usuario,
    db_update_usuario,
    db_delete_usuario,
    db_get_historial_libros,
    db_get_estadisticas_admin_panel_a,
    db_auth_usuario,
    db_get_last_id_usuario,
    db_get_all_usuarios, db_auth_admin
)
from app.models.db_models import Usuario

router = APIRouter(
    prefix="/usuario",
    tags=["Usuarios"],  # Grouped under "Usuarios" in Swagger UI
)

@router.get("/get_panel_a_estadisticas", response_model={}, summary="Get panel A statistics")
@router.get("/get_panel_a_estadisticas/", response_model={}, summary="Get panel A statistics")
def api_db_get_estadisticas_admin_panel_a():
    """
    Fetch a single usuario by its ID.

    - **pk_id_usuario**: The ID of the user to fetch.
    """
    try:
        return db_get_estadisticas_admin_panel_a()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/all", response_model=List[Usuario], summary="Get panel A statistics")
@router.get("/all/", response_model=List[Usuario], summary="Get panel A statistics")
def api_db_get_all_usuarios():
    """
    Fetch a single usuario by its ID.

    - **pk_id_usuario**: The ID of the user to fetch.
    """
    try:
        return db_get_all_usuarios()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/ultimo_usuario_id", response_model=int, summary="Get last registered pk_id_usuario from users")
@router.get("/ultimo_usuario_id/", response_model=int, summary="Get last registered pk_id_usuario from users")
def api_db_get_estadisticas_admin_panel_a():
    """
    Fetch a single usuario by its ID.

    - **pk_id_usuario**: The ID of the user to fetch.
    """
    try:
        return db_get_last_id_usuario()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/validation", response_model=Usuario, summary="Get a Usuario by ID")
@router.get("/validation/", response_model=Usuario, summary="Get a Usuario by ID")
def api_db_auth_usuario(email: str, password: str):
    try:
        # Intentamos la autenticación
        usuario = db_auth_usuario(email, password)    
        # Si db_auth_usuario retorna None por lógica interna
        if usuario is None:
            raise HTTPException(status_code=401, detail="No autorizado")
        return usuario
    except ClientResponseError as e:
        # Si PocketBase lanzó 400 o 404, nosotros respondemos 401
        raise HTTPException(
            status_code=401, 
            detail="Credenciales inválidas o usuario no encontrado"
        )
    except Exception as e:
        # Para cualquier otro error (conexión, base de datos caída, etc.)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/validation_admin", response_model=Usuario, summary="Get a Usuario by ID")
@router.get("/validation_admin/", response_model=Usuario, summary="Get a Usuario by ID")
def api_db_auth_admin(email: str, password: str):
    """
    Fetch a single usuario by its ID.

    - **pk_id_usuario**: The ID of the user to fetch.
    """
    try:
        return db_auth_admin(email, password)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{pk_id_usuario}", response_model=Usuario, summary="Get a Usuario by ID")
def api_get_usuario(pk_id_usuario: int):
    """
    Fetch a single usuario by its ID.

    - **pk_id_usuario**: The ID of the user to fetch.
    """
    try:
        return db_get_usuario(pk_id_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/create", response_model=Usuario, summary="Create a new Usuario")
@router.post("/create/", response_model=Usuario, summary="Create a new Usuario")
def api_create_usuario(usuario: Usuario):
    """
    Create a new usuario, password longger than 8 characters.
    """
    try:
        return db_create_usuario(usuario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update/", response_model=Usuario, summary="Update a Usuario")
@router.patch("/update", response_model=Usuario, summary="Update a Usuario")
def api_update_usuario(usuario: Usuario):
    """
    Update an existing usuario, requires password and confirmation.
    """
    try:
        return db_update_usuario(usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{pk_id_usuario}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Usuario by ID")
def api_delete_usuario(pk_id_usuario: int):
    """
    Delete a usuario by its ID.

    - **pk_id_usuario**: The ID of the user to delete.
    """
    try:
        db_delete_usuario(pk_id_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/get/historial/{pk_id_usuario}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Usuario by ID")
def api_delete_usuario(pk_id_usuario: int):
    """
    Delete a usuario by its ID.

    - **pk_id_usuario**: The ID of the user to delete.
    """
    try:
        db_get_historial_libros(pk_id_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))