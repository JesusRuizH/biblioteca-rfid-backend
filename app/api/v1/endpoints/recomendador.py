from fastapi import APIRouter, HTTPException

from app.models.expert_models import RespuestaUsuario, SesionInicio, TurnoRecomendador
from app.services.libro_expert_service import (
    get_expert_system,
    reset_expert_system,
    hidratar_top3,
)

router = APIRouter(
    prefix="/recomendador",
    tags=["Recomendador"],
)


@router.post(
    "/sesion",
    response_model=SesionInicio,
    summary="Inicia una nueva sesión del recomendador",
)
def iniciar_sesion():
    """
    Crea una sesión nueva y devuelve la primera pregunta con sus opciones.
    El frontend debe guardar `sesion_id` para los turnos siguientes.
    """
    try:
        expert = get_expert_system()
        sesion_id, info = expert.nueva_sesion()
        return SesionInicio(sesion_id=sesion_id, **info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/responder",
    response_model=TurnoRecomendador,
    summary="Envía una respuesta y recibe la siguiente pregunta o el top 3 de libros",
)
def responder(respuesta: RespuestaUsuario):
    """
    Recibe la respuesta del usuario para la pregunta actual.

    - `finalizado=False` → devuelve la siguiente pregunta con opciones y progreso.
    - `finalizado=True`  → devuelve top 3 libros con porcentaje de confianza y explicación.
    """
    try:
        expert = get_expert_system()
        resultado = expert.responder(
            sesion_id=respuesta.sesion_id,
            clave=respuesta.clave,
            valor=respuesta.valor,
        )

        if resultado["finalizado"]:
            top3_hidratado = hidratar_top3(resultado["top3"])
            return TurnoRecomendador(
                sesion_id=respuesta.sesion_id,
                finalizado=True,
                top3=top3_hidratado,
                explicacion=resultado["explicacion"],
                modo=resultado["modo"],
                entrenado_con=resultado["entrenado_con"],
            )

        return TurnoRecomendador(
            sesion_id=respuesta.sesion_id,
            finalizado=False,
            pregunta=resultado["pregunta"],
            clave=resultado["clave"],
            opciones=resultado["opciones"],
            progreso=resultado["progreso"],
            total=resultado["total"],
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/recargar",
    summary="Re-entrena el sistema experto con los datos actuales de la BD",
)
def recargar():
    """
    Fuerza el re-entrenamiento del árbol de decisión.
    Útil cuando se agregan libros o géneros nuevos sin reiniciar el servidor.
    """
    try:
        reset_expert_system()
        get_expert_system()
        return {"mensaje": "Sistema re-entrenado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))